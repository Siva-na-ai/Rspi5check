"""
utils/camera.py
Handles opening Pi Camera (via libcamera GStreamer pipeline)
and standard video sources (webcam, file, RTSP).
"""

import cv2
from config.settings import Settings


def open_picamera(cfg: Settings):
    """
    Open Raspberry Pi Camera using libcamera via GStreamer.
    Falls back to v4l2 device if GStreamer pipeline fails.
    """
    w, h, fps = cfg.RPI_CAM_WIDTH, cfg.RPI_CAM_HEIGHT, cfg.RPI_CAM_FPS

    # ── Try libcamera GStreamer pipeline first ─────────────────────
    gst_pipeline = (
        f"libcamerasrc ! "
        f"video/x-raw,width={w},height={h},framerate={fps}/1 ! "
        f"videoconvert ! "
        f"video/x-raw,format=BGR ! "
        f"appsink drop=1"
    )

    print(f"[INFO] Trying Pi Camera via GStreamer: {gst_pipeline}")
    cap = cv2.VideoCapture(gst_pipeline, cv2.CAP_GSTREAMER)

    if cap.isOpened():
        print("[INFO] Pi Camera opened via libcamera GStreamer pipeline.")
        return cap

    # ── Fallback: v4l2 device (/dev/video0) ───────────────────────
    print("[WARN] GStreamer pipeline failed. Falling back to /dev/video0 ...")
    cap = cv2.VideoCapture(0)

    if cap.isOpened():
        cap.set(cv2.CAP_PROP_FRAME_WIDTH,  w)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h)
        cap.set(cv2.CAP_PROP_FPS, fps)
        print("[INFO] Pi Camera opened via v4l2 (/dev/video0).")
        return cap

    print("[ERROR] Could not open Pi Camera via any method.")
    return None


def open_source(source: str):
    """
    Open a standard video source:
      - Integer string "0", "1" → webcam index
      - File path              → video file
      - rtsp:// / http://      → IP camera / stream
    """
    if source.isdigit():
        idx = int(source)
        print(f"[INFO] Opening webcam index: {idx}")
        cap = cv2.VideoCapture(idx)
    else:
        print(f"[INFO] Opening source: {source}")
        cap = cv2.VideoCapture(source)

    if not cap.isOpened():
        print(f"[ERROR] Failed to open source: {source}")
        return None

    return cap
