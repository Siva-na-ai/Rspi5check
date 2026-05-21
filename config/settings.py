"""
config/settings.py
Central configuration — edit this file to tune the tracker.
Raspberry Pi optimized defaults.
"""

import platform
import os


def _is_raspberry_pi() -> bool:
    """Auto-detect if running on a Raspberry Pi."""
    try:
        with open("/proc/cpuinfo", "r") as f:
            return "Raspberry Pi" in f.read()
    except Exception:
        return False


IS_RPI = _is_raspberry_pi()


class Settings:
    # ── Model ──────────────────────────────────────────────────────
    MODEL_PATH: str = "models/yolo11n.pt"   # auto-downloaded if missing

    # ── Detection ──────────────────────────────────────────────────
    CONF_THRESHOLD: float = 0.40    # detection confidence
    IOU_THRESHOLD: float  = 0.50    # NMS IoU threshold
    PERSON_CLASS: int     = 0       # COCO class 0 = person

    # ── Tracker ────────────────────────────────────────────────────
    TRACKER: str = "bytetrack.yaml"   # or "botsort.yaml"

    # ── Source ─────────────────────────────────────────────────────
    # "0"         → USB/default webcam
    # "picamera"  → Raspberry Pi Camera (libcamera)
    # "path/to/video.mp4" → video file
    # "rtsp://..."        → IP camera
    SOURCE: str = "picamera" if IS_RPI else "0"

    # ── Inference size ─────────────────────────────────────────────
    # 320 → faster, less accurate  (recommended for RPi)
    # 640 → slower, more accurate  (recommended for desktop/server)
    IMGSZ: int = 320 if IS_RPI else 640

    # ── Display ────────────────────────────────────────────────────
    SHOW: bool  = True    # show live OpenCV window
    SAVE: bool  = False   # save annotated video to output/

    # ── Output paths ───────────────────────────────────────────────
    OUTPUT_DIR: str  = "output"
    OUTPUT_FILE: str = "output/tracked_output.mp4"
    LOG_DIR: str     = "logs"

    # ── Logging ────────────────────────────────────────────────────
    LOG: bool = False   # save per-frame CSV log to logs/

    # ── Raspberry Pi Camera resolution ─────────────────────────────
    RPI_CAM_WIDTH: int  = 640
    RPI_CAM_HEIGHT: int = 480
    RPI_CAM_FPS: int    = 30

    def __str__(self):
        return (
            "\n══════════════════════════════════════\n"
            f"  Person Tracker — Settings\n"
            "══════════════════════════════════════\n"
            f"  Platform  : {'Raspberry Pi' if IS_RPI else platform.system()}\n"
            f"  Model     : {self.MODEL_PATH}\n"
            f"  Source    : {self.SOURCE}\n"
            f"  Img size  : {self.IMGSZ}\n"
            f"  Conf      : {self.CONF_THRESHOLD}\n"
            f"  Tracker   : {self.TRACKER}\n"
            f"  Show      : {self.SHOW}\n"
            f"  Save      : {self.SAVE}\n"
            f"  Log CSV   : {self.LOG}\n"
            "══════════════════════════════════════"
        )
