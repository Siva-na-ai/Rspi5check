"""
utils/colors.py
Maps tracker IDs to consistent, visually distinct BGR colors
using golden-angle hue spacing in HSV color space.
"""

import cv2
import numpy as np


def id_to_color(tid: int) -> tuple:
    """
    Returns a consistent BGR color for a given tracker ID.
    Uses golden-ratio hue spacing so colors are maximally distinct.
    """
    hue = int((tid * 137.508) % 360)   # golden-angle step
    hsv_pixel = np.uint8([[[hue // 2, 220, 220]]])
    bgr = cv2.cvtColor(hsv_pixel, cv2.COLOR_HSV2BGR)[0][0]
    return (int(bgr[0]), int(bgr[1]), int(bgr[2]))
