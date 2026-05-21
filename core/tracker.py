"""
core/tracker.py
Main PersonTracker class — handles:
  • Pi Camera (libcamera) and standard webcam/video sources
  • YOLOv11n inference + ByteTrack tracking
  • Unique person ID assignment and counting
  • HUD overlay rendering
  • CSV logging
  • Video saving
"""

import cv2
import os
import time
import numpy as np
from ultralytics import YOLO

from config.settings import Settings, IS_RPI
from utils.colors import id_to_color
from utils.hud import draw_hud
from utils.logger import FrameLogger
from utils.camera import open_picamera, open_source


class PersonTracker:
    def __init__(self, cfg: Settings):
        self.cfg = cfg
        os.makedirs(cfg.OUTPUT_DIR, exist_ok=True)
        os.makedirs(cfg.LOG_DIR, exist_ok=True)

        print(f"[INFO] Loading model: {cfg.MODEL_PATH}")
        self.model = YOLO(cfg.MODEL_PATH)

        self.all_ids: set = set()          # all unique IDs ever seen
        self.frame_idx: int = 0
        self.logger = FrameLogger(cfg.LOG_DIR) if cfg.LOG else None
        self.writer = None

    # ──────────────────────────────────────────────────────────────
    def run(self):
        cfg = self.cfg

        # ── Open camera / video source ────────────────────────────
        if cfg.SOURCE.lower() == "picamera":
            cap = open_picamera(cfg)
        else:
            cap = open_source(cfg.SOURCE)

        if cap is None or not cap.isOpened():
            raise RuntimeError(f"[ERROR] Cannot open source: {cfg.SOURCE}")

        fps    = cap.get(cv2.CAP_PROP_FPS) or 30
        width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        print(f"[INFO] Stream: {width}x{height} @ {fps:.1f} FPS")

        # ── Video writer ──────────────────────────────────────────
        if cfg.SAVE:
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            self.writer = cv2.VideoWriter(
                cfg.OUTPUT_FILE, fourcc, fps, (width, height)
            )
            print(f"[INFO] Saving output to: {cfg.OUTPUT_FILE}")

        print("[INFO] Tracker running — press Q to quit\n")

        t_start = time.time()

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("[WARN] Frame read failed — end of stream or camera error.")
                    break

                frame = self._process_frame(frame)

                if cfg.SHOW:
                    cv2.imshow("Person Tracker", frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        print("[INFO] Quit key pressed.")
                        break

                if self.writer:
                    self.writer.write(frame)

                self.frame_idx += 1

        except KeyboardInterrupt:
            print("\n[INFO] Interrupted by user.")

        finally:
            self._cleanup(cap, t_start)

    # ──────────────────────────────────────────────────────────────
    def _process_frame(self, frame: np.ndarray) -> np.ndarray:
        cfg = self.cfg
        current_ids: set = set()

        # ── Run YOLO tracking ─────────────────────────────────────
        results = self.model.track(
            frame,
            persist=True,
            conf=cfg.CONF_THRESHOLD,
            iou=cfg.IOU_THRESHOLD,
            classes=[cfg.PERSON_CLASS],
            tracker=cfg.TRACKER,
            imgsz=cfg.IMGSZ,
            verbose=False,
        )

        # ── Parse results ─────────────────────────────────────────
        if (results[0].boxes is not None
                and results[0].boxes.id is not None):

            boxes = results[0].boxes.xyxy.cpu().numpy()
            ids   = results[0].boxes.id.cpu().numpy().astype(int)
            confs = results[0].boxes.conf.cpu().numpy()

            for box, tid, conf in zip(boxes, ids, confs):
                x1, y1, x2, y2 = map(int, box)
                self.all_ids.add(tid)
                current_ids.add(tid)
                self._draw_person(frame, x1, y1, x2, y2, tid, conf)

        # ── HUD overlay ───────────────────────────────────────────
        draw_hud(frame, len(current_ids), len(self.all_ids), self.frame_idx)

        # ── Log ───────────────────────────────────────────────────
        if self.logger:
            self.logger.log(self.frame_idx, current_ids, self.all_ids)

        return frame

    # ──────────────────────────────────────────────────────────────
    def _draw_person(self, frame, x1, y1, x2, y2, tid, conf):
        color = id_to_color(tid)

        # Bounding box
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

        # Label background + text
        label = f"ID {tid}  {conf:.2f}"
        (lw, lh), base = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2
        )
        cv2.rectangle(
            frame,
            (x1, y1 - lh - base - 4),
            (x1 + lw + 4, y1),
            color, -1,
        )
        cv2.putText(
            frame, label,
            (x1 + 2, y1 - base - 2),
            cv2.FONT_HERSHEY_SIMPLEX, 0.55,
            (255, 255, 255), 2, cv2.LINE_AA,
        )

    # ──────────────────────────────────────────────────────────────
    def _cleanup(self, cap, t_start):
        cap.release()
        if self.writer:
            self.writer.release()
        cv2.destroyAllWindows()

        if self.logger:
            self.logger.close()

        elapsed = time.time() - t_start
        avg_fps = self.frame_idx / elapsed if elapsed > 0 else 0

        print("\n" + "═" * 50)
        print("  TRACKING SUMMARY")
        print("═" * 50)
        print(f"  Frames processed : {self.frame_idx}")
        print(f"  Elapsed time     : {elapsed:.1f}s")
        print(f"  Average FPS      : {avg_fps:.1f}")
        print(f"  Unique persons   : {len(self.all_ids)}")
        print(f"  Person IDs       : {sorted(self.all_ids)}")
        print("═" * 50)
