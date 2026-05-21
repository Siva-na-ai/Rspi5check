"""
Person Tracker — Entry Point
Raspberry Pi + Pi Camera compatible
"""

import argparse
import sys
from core.tracker import PersonTracker
from config.settings import Settings


def parse_args():
    parser = argparse.ArgumentParser(
        description="YOLOv11n Person Detection + Unique ID Tracker (RPi Compatible)"
    )
    parser.add_argument(
        "--source", type=str, default=None,
        help="Video file path, webcam index (0), RTSP URL, or 'picamera' for Pi Cam"
    )
    parser.add_argument(
        "--show", action="store_true", default=True,
        help="Display live annotated stream window"
    )
    parser.add_argument(
        "--no-show", action="store_true", default=False,
        help="Disable live window (headless / server mode)"
    )
    parser.add_argument(
        "--save", action="store_true", default=False,
        help="Save annotated output video"
    )
    parser.add_argument(
        "--imgsz", type=int, default=None,
        help="Inference image size (default: 320 for RPi, 640 for others)"
    )
    parser.add_argument(
        "--conf", type=float, default=None,
        help="Detection confidence threshold (default from settings)"
    )
    parser.add_argument(
        "--log", action="store_true", default=False,
        help="Save CSV log of detections per frame"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Load settings
    cfg = Settings()

    # Override from CLI if provided
    if args.source is not None:
        cfg.SOURCE = args.source
    if args.imgsz is not None:
        cfg.IMGSZ = args.imgsz
    if args.conf is not None:
        cfg.CONF_THRESHOLD = args.conf
    if args.no_show:
        cfg.SHOW = False
    else:
        cfg.SHOW = args.show
    cfg.SAVE  = args.save
    cfg.LOG   = args.log

    print(cfg)

    tracker = PersonTracker(cfg)
    tracker.run()


if __name__ == "__main__":
    main()
