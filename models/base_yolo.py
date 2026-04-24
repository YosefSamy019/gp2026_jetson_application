import os

import cv2
import onnxruntime as ort
import numpy as np
import json
import mcal.logs as logs


class YOLODetector:
    def __init__(self, model_path, classes_path):
        """
        Initialize the detector.
        :param model_path: Path to .onnx file
        :param classes_path: Path to .json classes file
        """
        self.model_name = os.path.split(model_path)[-1]
        self.input_shape = (640, 640)

        try:
            # Detect available providers
            available_providers = ort.get_available_providers()

            # Build provider priority (GPU first)
            self.providers = []

            if "CUDAExecutionProvider" in available_providers:
                self.providers.append("CUDAExecutionProvider")
                logs.add_log(
                    f"Load {self.model_name} on GPU",
                    logs.LogLevel.INFO
                )
            else:
                # CPU fallback always
                self.providers.append("CPUExecutionProvider")
                logs.add_log(
                    f"Load {self.model_name} on CPU",
                    logs.LogLevel.INFO
                )

            # Initialize ONNX session
            self.session = ort.InferenceSession(
                model_path,
                providers=self.providers
            )

            self.input_name = self.session.get_inputs()[0].name

            # Load class names
            with open(classes_path, "r") as f:
                self.class_names = json.load(f)

            logs.add_log(
                "Model {} initialized. {} classes loaded.".format(
                    model_path, len(self.class_names)
                ),
                logs.LogLevel.INFO
            )

            logs.add_log(
                "Active ONNX providers: {}".format(self.session.get_providers()),
                logs.LogLevel.INFO
            )

        except Exception as e:
            logs.add_log(
                "Failed to initialize YOLODetector: {}".format(e),
                logs.LogLevel.ERROR
            )
            self.session = None

    def _letterbox(self, img, color=(114, 114, 114)):
        """Internal helper for resizing and padding."""
        h, w = img.shape[:2]
        new_w, new_h = self.input_shape
        r = min(new_w / w, new_h / h)

        new_unpad = (int(round(w * r)), int(round(h * r)))
        dw, dh = (new_w - new_unpad[0]) / 2, (new_h - new_unpad[1]) / 2

        img_resized = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)

        top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
        left, right = int(round(dw - 0.1)), int(round(dw + 0.1))

        img_padded = cv2.copyMakeBorder(img_resized, top, bottom, left, right,
                                        cv2.BORDER_CONSTANT, value=color)
        return img_padded, r, dw, dh

    def detect(self, image: np.ndarray, conf_threshold=0.5, iou_threshold=0.4):
        """
        Main inference method.
        """
        if self.session is None:
            return []

        orig_h, orig_w = image.shape[:2]

        # 1. Pre-process
        img_padded, r, dw, dh = self._letterbox(image)
        # BGR to RGB, HWC to CHW, Normalize
        blob = img_padded[:, :, ::-1].transpose(2, 0, 1)
        blob = np.expand_dims(blob, axis=0).astype(np.float32) / 255.0

        # 2. Run Inference
        outputs = self.session.run(None, {self.input_name: blob})
        predictions = outputs[0][0]  # (300, 6)
        # print(predictions)
        # 3. Filter for NMS
        raw_boxes, scores, class_ids = [], [], []
        for line in predictions:
            x1, y1, x2, y2, score, class_idx = line
            if score > conf_threshold:
                w, h = x2 - x1, y2 - y1
                raw_boxes.append([float(x1), float(y1), float(w), float(h)])
                scores.append(float(score))
                class_ids.append(int(class_idx))

        # 4. OpenCV NMS (IOU Filter)
        indices = cv2.dnn.NMSBoxes(raw_boxes, scores, conf_threshold, iou_threshold)

        final_results = []
        if len(indices) > 0:
            for i in indices.flatten():
                x, y, w, h = raw_boxes[i]

                # 5. Scale back to original coordinates
                rx1 = (x - dw) / r
                ry1 = (y - dh) / r
                rx2 = (x + w - dw) / r
                ry2 = (y + h - dh) / r

                final_results.append({
                    "class": self.class_names.get(str(class_ids[i]), "Unknown"),
                    "score": round(scores[i], 2),
                    "box": [
                        max(0, int(rx1)), max(0, int(ry1)),
                        min(orig_w, int(rx2)), min(orig_h, int(ry2))
                    ]
                })

        return final_results

    def __call__(self, image, **kwargs):
        """Allows calling the object like a function: detector(image)"""
        return self.detect(image, **kwargs)
