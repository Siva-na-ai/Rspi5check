"""
utils/logger.py
Logs per-frame detection data to a CSV file in logs/ directory.
Enabled via --log flag or cfg.LOG = True.
"""

import csv
import os
from datetime import datetime


class FrameLogger:
    def __init__(self, log_dir: str):
        os.makedirs(log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filepath = os.path.join(log_dir, f"tracking_{timestamp}.csv")

        self._file = open(self.filepath, "w", newline="")
        self._writer = csv.writer(self._file)
        self._writer.writerow([
            "frame", "active_count", "active_ids", "unique_total"
        ])
        print(f"[INFO] CSV log: {self.filepath}")

    def log(self, frame_idx: int, current_ids: set, all_ids: set):
        self._writer.writerow([
            frame_idx,
            len(current_ids),
            ";".join(str(i) for i in sorted(current_ids)),
            len(all_ids),
        ])

    def close(self):
        self._file.flush()
        self._file.close()
        print(f"[INFO] Log saved: {self.filepath}")
