# Person Tracker — YOLOv11n + ByteTrack

Detects people in a video stream, assigns each a **unique ID**, and counts
how many unique individuals have appeared — optimized for both desktop and
Raspberry Pi + Pi Camera.

---

## Folder Structure

```
person_tracker/
│
├── main.py                   ← Entry point (run this)
│
├── config/
│   ├── __init__.py
│   └── settings.py           ← All config (model, thresholds, source, etc.)
│
├── core/
│   ├── __init__.py
│   └── tracker.py            ← Main tracking loop (YOLO + ByteTrack)
│
├── utils/
│   ├── __init__.py
│   ├── camera.py             ← Pi Camera & standard source handling
│   ├── colors.py             ← ID → unique color mapping
│   ├── hud.py                ← On-screen HUD overlay
│   └── logger.py             ← CSV frame logger
│
├── models/                   ← yolo11n.pt auto-downloaded here
├── output/                   ← Saved annotated videos go here
├── logs/                     ← CSV logs go here (--log flag)
│
├── scripts/
│   └── setup_rpi.sh          ← One-shot RPi setup script
│
├── requirements.txt          ← Desktop / server install
└── requirements_rpi.txt      ← Raspberry Pi install
```

---

## Quick Start

### Desktop / PC

```bash
# Install
pip install -r requirements.txt

# Run on webcam
python main.py

# Run on video file
python main.py --source path/to/video.mp4

# Run on RTSP stream + save output
python main.py --source rtsp://192.168.1.10/stream --save

# Log per-frame CSV data
python main.py --log
```

### Raspberry Pi + Pi Camera

```bash
# One-shot setup (installs everything)
chmod +x scripts/setup_rpi.sh
./scripts/setup_rpi.sh

# Reboot if camera was just enabled
sudo reboot

# Run (Pi Camera auto-detected)
python main.py

# Headless mode (no display, save video)
python main.py --no-show --save

# Save + log CSV
python main.py --save --log
```

---

## CLI Arguments

| Flag | Default | Description |
|---|---|---|
| `--source` | `picamera` (RPi) / `0` (PC) | Video source |
| `--show` | `True` | Show live window |
| `--no-show` | `False` | Disable window (headless) |
| `--save` | `False` | Save annotated video to `output/` |
| `--imgsz` | `320` (RPi) / `640` (PC) | Inference image size |
| `--conf` | `0.40` | Detection confidence threshold |
| `--log` | `False` | Save CSV log to `logs/` |

---

## Configuration

Edit `config/settings.py` to change defaults permanently:

```python
MODEL_PATH     = "models/yolo11n.pt"   # swap to yolo11s.pt for more accuracy
CONF_THRESHOLD = 0.40
IOU_THRESHOLD  = 0.50
TRACKER        = "bytetrack.yaml"      # or "botsort.yaml"
IMGSZ          = 320                   # 320 (fast) or 640 (accurate)
```

---

## Expected FPS on Raspberry Pi

| Device | imgsz=640 | imgsz=320 |
|---|---|---|
| RPi 4 (4 GB) | ~2–4 FPS | ~6–10 FPS |
| RPi 5 (8 GB) | ~5–8 FPS | ~12–18 FPS |
| RPi 5 + Hailo AI Hat | ~30+ FPS | ~30+ FPS |

> For people-counting use cases (entrance, room occupancy), 5–10 FPS is sufficient.

---

## Press **Q** to quit the live window.
