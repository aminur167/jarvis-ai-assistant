# -*- coding: utf-8 -*-
import ctypes
import json
import subprocess
from datetime import datetime
from pathlib import Path


VK_VOLUME_MUTE = 0xAD
VK_VOLUME_DOWN = 0xAE
VK_VOLUME_UP = 0xAF
KEYEVENTF_KEYUP = 0x0002


def _press_key(key_code, times=1):
    user32 = ctypes.windll.user32
    for _ in range(times):
        user32.keybd_event(key_code, 0, 0, 0)
        user32.keybd_event(key_code, 0, KEYEVENTF_KEYUP, 0)


def _battery_status():
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        "(Get-CimInstance Win32_Battery | Select-Object -First 1 EstimatedChargeRemaining,BatteryStatus | ConvertTo-Json -Compress)",
    ]
    result = subprocess.run(command, capture_output=True, text=True, timeout=5)
    output = result.stdout.strip()
    if not output:
        return "Battery information is not available on this device."
    try:
        data = json.loads(output)
        percentage = data.get("EstimatedChargeRemaining")
        status = data.get("BatteryStatus")
        if percentage is None:
            return "Battery information is not available on this device."
        charging_text = "charging" if status == 2 else "not charging"
        return f"Battery is at {percentage} percent and {charging_text}."
    except Exception:
        return f"Battery status: {output}"


def _take_screenshot():
    screenshots_dir = Path.home() / "Pictures" / "Jarvis Screenshots"
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    filename = screenshots_dir / f"screenshot-{datetime.now().strftime('%Y%m%d-%H%M%S')}.png"

    ps_script = f"""
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$bounds = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
$bitmap = New-Object System.Drawing.Bitmap $bounds.Width, $bounds.Height
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.CopyFromScreen($bounds.Location, [System.Drawing.Point]::Empty, $bounds.Size)
$bitmap.Save('{filename}', [System.Drawing.Imaging.ImageFormat]::Png)
$graphics.Dispose()
$bitmap.Dispose()
"""
    subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], check=True, timeout=10)
    return f"Screenshot saved to {filename}"


def handle_system_control(command):
    command = command.lower().strip()

    try:
        if command in ("volume up", "increase volume", "sound up"):
            _press_key(VK_VOLUME_UP, times=5)
            return True, "Volume increased."
        if command in ("volume down", "decrease volume", "sound down"):
            _press_key(VK_VOLUME_DOWN, times=5)
            return True, "Volume decreased."
        if command in ("mute", "mute volume"):
            _press_key(VK_VOLUME_MUTE)
            return True, "Volume muted."
        if command in ("unmute", "unmute volume"):
            _press_key(VK_VOLUME_MUTE)
            return True, "Volume toggled."
        if command in ("battery", "battery status", "battery percentage"):
            return True, _battery_status()
        if command in ("screenshot", "take screenshot", "capture screen"):
            return True, _take_screenshot()
        if command == "shutdown confirm":
            subprocess.Popen(["shutdown", "/s", "/t", "30"])
            return True, "Shutdown scheduled in 30 seconds."
        if command == "restart confirm":
            subprocess.Popen(["shutdown", "/r", "/t", "30"])
            return True, "Restart scheduled in 30 seconds."
        if command in ("shutdown", "restart"):
            return True, f"Please say {command} confirm if you really want to {command}."
    except Exception:
        return True, "Sorry, I could not control the system right now."

    return False, None
