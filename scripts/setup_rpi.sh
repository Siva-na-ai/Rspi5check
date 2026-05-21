#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# scripts/setup_rpi.sh
# One-shot setup script for Raspberry Pi
# Run: chmod +x scripts/setup_rpi.sh && ./scripts/setup_rpi.sh
# ═══════════════════════════════════════════════════════════════

set -e

echo ""
echo "══════════════════════════════════════════"
echo "  Person Tracker — Raspberry Pi Setup"
echo "══════════════════════════════════════════"
echo ""

# ── 1. System packages ─────────────────────────────────────────
echo "[1/4] Installing system packages..."
sudo apt update -qq
sudo apt install -y \
    python3-pip \
    python3-opencv \
    libopencv-dev \
    libcamera-dev \
    libcamera-apps \
    libgstreamer1.0-dev \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-libav \
    v4l-utils

# ── 2. Enable camera interface ─────────────────────────────────
echo "[2/4] Enabling camera interface..."
if ! grep -q "camera_auto_detect=1" /boot/config.txt 2>/dev/null; then
    echo "camera_auto_detect=1" | sudo tee -a /boot/config.txt
fi

# ── 3. Python packages ─────────────────────────────────────────
echo "[3/4] Installing Python packages..."
pip install --break-system-packages -r requirements_rpi.txt

# ── 4. Create output directories ──────────────────────────────
echo "[4/4] Creating output directories..."
mkdir -p output logs models

echo ""
echo "══════════════════════════════════════════"
echo "  Setup complete!"
echo ""
echo "  Test Pi Camera:"
echo "    libcamera-hello --timeout 3000"
echo ""
echo "  Run tracker:"
echo "    python main.py"
echo ""
echo "  NOTE: Reboot if camera was just enabled:"
echo "    sudo reboot"
echo "══════════════════════════════════════════"
