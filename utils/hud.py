"""
utils/hud.py
Draws the semi-transparent HUD panel on each frame.
Shows: frame number, active persons, unique total.
"""

import cv2
import numpy as np


def draw_hud(frame: np.ndarray, active: int, total: int, frame_idx: int):
    """
    Renders a semi-transparent info panel in the top-left corner.

    Args:
        frame     : BGR frame to draw on (in-place)
        active    : number of persons visible in current frame
        total     : cumulative unique persons detected so far
        frame_idx : current frame number
    """
    panel_w, panel_h = 295, 100
    x0, y0 = 10, 10

    # Semi-transparent dark background
    overlay = frame.copy()
    cv2.rectangle(
        overlay,
        (x0, y0),
        (x0 + panel_w, y0 + panel_h),
        (15, 15, 15), -1
    )
    cv2.addWeighted(overlay, 0.60, frame, 0.40, 0, frame)

    # Accent bar on left edge
    cv2.rectangle(
        frame,
        (x0, y0),
        (x0 + 4, y0 + panel_h),
        (0, 255, 140), -1
    )

    lines = [
        ("Frame",        str(frame_idx)),
        ("Active now",   f"{active} person(s)"),
        ("Unique total", f"{total} person(s)"),
    ]

    for i, (label, value) in enumerate(lines):
        y = y0 + 28 + i * 24

        # Label (dim)
        cv2.putText(
            frame, f"{label}:",
            (x0 + 12, y),
            cv2.FONT_HERSHEY_SIMPLEX, 0.50,
            (160, 160, 160), 1, cv2.LINE_AA,
        )
        # Value (bright)
        cv2.putText(
            frame, value,
            (x0 + 145, y),
            cv2.FONT_HERSHEY_SIMPLEX, 0.52,
            (0, 255, 140), 1, cv2.LINE_AA,
        )
