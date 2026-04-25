import os
import cv2
import onnxruntime as ort
import numpy as np
import json
import mcal.logs as logs


class YOLODetector:
    def __init__(self, model_path, classes_path):
        self.model_name = os.path.split(model_path)[-1]
        self.input_shape = (640, 640)

        try:
            available_providers = ort.get_available_providers()
            self.providers = (
                ["CUDAExecutionProvider"]
                if "CUDAExecutionProvider" in available_providers
                else ["CPUExecutionProvider"]
            )

            logs.add_log(
                f"Load {self.model_name} on {self.providers[0]}",
                logs.LogLevel.INFO
            )

            self.session = ort.InferenceSession(
                model_path,
                providers=self.providers
            )

            # Get input details
            model_input = self.session.get_inputs()[0]
            self.input_name = model_input.name
            self.input_type = model_input.type  # Store this to check for FP16 vs FP32

            with open(classes_path, "r") as f:
                self.class_names = json.load(f)

            logs.add_log(
                f"Model {self.model_name} initialized. {len(self.class_names)} classes loaded. Type: {self.input_type}",
                logs.LogLevel.INFO
            )

        except Exception as e:
            logs.add_log(f"Init failed: {e}", logs.LogLevel.ERROR)
            self.session = None

    # -------------------------
    def _letterbox(self, img, color=(114, 114, 114)):
        h, w = img.shape[:2]
        new_w, new_h = self.input_shape

        r = min(new_w / w, new_h / h)
        new_unpad = (int(round(w * r)), int(round(h * r)))

        dw = (new_w - new_unpad[0]) / 2
        dh = (new_h - new_unpad[1]) / 2

        img_resized = cv2.resize(img, new_unpad, interpolation=cv2.INTER_LINEAR)

        top, bottom = int(round(dh)), int(round(dh))
        left, right = int(round(dw)), int(round(dw))

        img_padded = cv2.copyMakeBorder(
            img_resized,
            top, bottom, left, right,
            cv2.BORDER_CONSTANT,
            value=color
        )

        return img_padded, r, dw, dh

    # -------------------------
    def detect(self, image: np.ndarray, conf_threshold=0.5, iou_threshold=0.4):
        if self.session is None:
            return []

        orig_h, orig_w = image.shape[:2]

        # 1. Preprocess
        img, r, dw, dh = self._letterbox(image)

        blob = img[:, :, ::-1].transpose(2, 0, 1)

        # FIX 1: Dynamically handle FP16 vs FP32 based on the ONNX model's expected type
        if "float16" in self.input_type:
            blob = np.expand_dims(blob, 0).astype(np.float16) / np.float16(255.0)
        else:
            blob = np.expand_dims(blob, 0).astype(np.float32) / 255.0

        # 2. Inference
        outputs = self.session.run(None, {self.input_name: blob})
        pred = outputs[0]

        # 3. reshape YOLOv8 ONNX output
        pred = np.squeeze(pred, 0).T  # (8400, 84)

        # 4. split
        boxes = pred[:, :4]

        # FIX 2: These are already probabilities! No sigmoid needed.
        class_probs = pred[:, 4:]

        class_ids = np.argmax(class_probs, axis=1)
        scores = np.max(class_probs, axis=1)

        # 6. filter
        mask = scores > conf_threshold

        boxes = boxes[mask]
        scores = scores[mask]
        class_ids = class_ids[mask]

        if len(boxes) == 0:
            return []

        # 7. convert to xyxy
        x = boxes[:, 0]
        y = boxes[:, 1]
        w = boxes[:, 2]
        h = boxes[:, 3]

        x1 = x - w / 2
        y1 = y - h / 2
        x2 = x + w / 2
        y2 = y + h / 2

        # 8. scale back to original image
        x1 = (x1 - dw) / r
        y1 = (y1 - dh) / r
        x2 = (x2 - dw) / r
        y2 = (y2 - dh) / r

        # cv2.dnn.NMSBoxes expects [top_left_x, top_left_y, width, height]
        boxes_cv = np.stack([x1, y1, x2 - x1, y2 - y1], axis=1).tolist()

        # 9. NMS
        idxs = cv2.dnn.NMSBoxes(
            boxes_cv,
            scores.tolist(),
            conf_threshold,
            iou_threshold
        )

        results = []

        if len(idxs) > 0:
            for i in idxs.flatten():
                x1_i, y1_i, w_i, h_i = boxes_cv[i]

                results.append({
                    "class": self.class_names.get(str(class_ids[i]), "Unknown"),
                    "score": float(scores[i]),
                    "box": [
                        max(0, int(x1_i)),
                        max(0, int(y1_i)),
                        min(orig_w, int(x1_i + w_i)),
                        min(orig_h, int(y1_i + h_i))
                    ]
                })

        return results

    # -------------------------
    def __call__(self, image, **kwargs):
        return self.detect(image, **kwargs)