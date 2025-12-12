import time
import ctypes
import sys

from pynput import keyboard
import pystray
from PIL import Image, ImageDraw

from comtypes import CoInitialize, CoUninitialize
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
import json


def load_config(path="config.json"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        print("Config file missing or invalid, using defaults.")
        return None

config = load_config() or {}

# settings
TARGET_PROCESS = config.get("target_process", "chrome.exe")
VOLUME_STEP = config.get("volume_step", 0.05)

hk = config.get("hotkeys", {})

KEY_VOL_DOWN = keyboard.Key[hk.get("volume_down", "f2")]
KEY_VOL_UP   = keyboard.Key[hk.get("volume_up", "f3")]
KEY_PREV     = keyboard.Key[hk.get("previous", "f7")]
KEY_PLAYPAUSE = keyboard.Key[hk.get("play_pause", "f8")]
KEY_NEXT     = keyboard.Key[hk.get("next", "f9")]

VK_NEXT  = 0xB0
VK_PREV  = 0xB1
VK_PLAY  = 0xB3

SendInput = ctypes.windll.user32.keybd_event

hotkeys_enabled = True
listener = None

def chrome_volume(delta):
    try:
        CoInitialize()
    except:
        pass

    try:
        sessions = AudioUtilities.GetAllSessions()
    except:
        return

    for sess in sessions:
        proc = sess.Process
        if proc and proc.name().lower() == TARGET_PROCESS:
            try:
                vol = sess._ctl.QueryInterface(ISimpleAudioVolume)
                cur = float(vol.GetMasterVolume())
                new = max(0.0, min(1.0, cur + delta))
                vol.SetMasterVolume(new, None)
            except:
                pass

    try:
        CoUninitialize()
    except:
        pass


def media_key(vk):
    SendInput(vk, 0, 0, 0)
    time.sleep(0.03)
    SendInput(vk, 0, 2, 0)


def on_key(key):
    if not hotkeys_enabled:
        return
    try:
        if key == KEY_VOL_DOWN:
            chrome_volume(-VOLUME_STEP)
        elif key == KEY_VOL_UP:
            chrome_volume(VOLUME_STEP)
        elif key == KEY_PREV:
            media_key(VK_PREV)
        elif key == KEY_PLAYPAUSE:
            media_key(VK_PLAY)
        elif key == KEY_NEXT:
            media_key(VK_NEXT)
    except:
        pass


def start_listener():
    global listener
    listener = keyboard.Listener(on_press=on_key)
    listener.start()

def create_icon():
    """Create a visible tray icon (white circle on black)."""
    img = Image.new("RGB", (64, 64), "black")
    draw = ImageDraw.Draw(img)
    draw.ellipse((16, 16, 48, 48), fill="white")
    return img


def toggle(icon, item):
    global hotkeys_enabled
    hotkeys_enabled = not hotkeys_enabled

    icon.menu = pystray.Menu(
        pystray.MenuItem(
            "Enable Hotkeys" if not hotkeys_enabled else "Disable Hotkeys",
            toggle
        ),
        pystray.MenuItem("Quit", quit_app)
    )
    try:
        icon.update_menu()
    except:
        pass

def quit_app(icon, item):
    try:
        listener.stop()
    except:
        pass
    icon.stop()
    sys.exit(0)


def create_tray():
    return pystray.Icon(
        "ytmusic",
        create_icon(),
        "YT Music Controller",
        menu=pystray.Menu(
            pystray.MenuItem("Disable Hotkeys", toggle),
            pystray.MenuItem("Quit", quit_app)
        )
    )

if __name__ == "__main__":
    start_listener()
    create_tray().run()
