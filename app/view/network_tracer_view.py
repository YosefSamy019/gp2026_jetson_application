import json
import customtkinter as ctk
import app.upper_logic as up

txt_frame: ctk.CTkFrame | None = None
value_labels: dict[str, ctk.CTkLabel] = {}
_trace_id: str | None = None


def init():
    global _trace_id

    if _trace_id is None:
        _trace_id = up.variable_network.trace_add("write", _output_parser)


def destroy():
    global _trace_id, value_labels, txt_frame

    if _trace_id is not None:
        try:
            up.variable_network.trace_remove("write", _trace_id)
        except Exception:
            pass
        _trace_id = None

    value_labels.clear()
    txt_frame = None


def _output_parser(_, __, ___):
    global value_labels

    # Frame destroyed → ignore safely
    if not txt_frame or not txt_frame.winfo_exists():
        return

    value = up.variable_network.get()

    try:
        json_dict = json.loads(value)
    except Exception:
        return

    # Remove dead widgets from dict
    dead_keys = [
        k for k, lbl in value_labels.items()
        if not lbl.winfo_exists()
    ]
    for k in dead_keys:
        del value_labels[k]

    # Update / Create labels
    for k, v in json_dict.items():

        # Create once
        if k not in value_labels:
            row = len(value_labels)

            key_label = ctk.CTkLabel(
                txt_frame,
                text=k,
                font=ctk.CTkFont(size=15),
                anchor="w"
            )
            key_label.grid(
                row=row,
                column=0,
                sticky="w",
                padx=15,
                pady=6
            )

            value_label = ctk.CTkLabel(
                txt_frame,
                text=str(v),
                font=ctk.CTkFont(size=22, weight="bold"),
                anchor="e"
            )
            value_label.grid(
                row=row,
                column=1,
                sticky="e",
                padx=15,
                pady=6
            )

            value_labels[k] = value_label

        # Safe update
        label = value_labels[k]
        if label.winfo_exists():
            label.configure(text=str(v))


def show_network_history_window(
        root: ctk.CTk,
        main_frame_hook: ctk.CTkScrollableFrame,
):
    global txt_frame

    # Create frame only once
    if txt_frame and txt_frame.winfo_exists():
        return

    txt_frame = ctk.CTkFrame(
        main_frame_hook,
        corner_radius=15
    )
    txt_frame.pack(padx=20, pady=20, fill="x")

    txt_frame.grid_columnconfigure(0, weight=1)
    txt_frame.grid_columnconfigure(1, weight=1)

    # Attach trace when UI is visible
    init()
