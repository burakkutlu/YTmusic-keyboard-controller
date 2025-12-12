YT Music Controller (No-Media-Key Friendly Windows Tray App)

A small Windows tray application that lets you control YouTube Music inside Browser even if your keyboard does not have media keys.

The app adds global hotkeys for:

- Volume Up/Down (Chrome-only volume — does NOT change system volume)
- Play/Pause
- Previous Track
- Next Track

It also provides:

- A tiny tray icon
- Enable/Disable Hotkeys toggle
- Quit option
- Customizable settings via config.json

This app has no visible window, runs silently, and is ideal for gaming setups or minimal keyboards.

* Features

- Works even if your keyboard has no media keys

- Per-app volume control (Browser only)
    F2 -> Volume Down (Chrome/YT Music only)
    F3 -> Volume Up (Chrome/YT Music only)

- YouTube Music global media controls
    F7 -> Previous Track
    F8 -> Play / Pause
    F9 -> Next Track

- Runs silently in the system tray

- Config file for easy customization

- Toggle hotkeys ON/OFF from tray

- Quit the app from tray

- No external icon/image files required

- No console window

Perfect for when you're in a game and want full control over YT Music without alt-tabbing or using special keys.

* Configuration (config.json)

All settings are editable in:

config.json

Default file:
    {
        "target_process": "chrome.exe",
        "volume_step": 0.05,
        "hotkeys": {
            "volume_down": "f2",
            "volume_up": "f3",
            "previous": "f7",
            "play_pause": "f8",
            "next": "f9"
        }
    }

You can customize:

- Which application to control (Chrome/Brave/etc.)
- The volume step
- Every hotkey


* Building the EXE 

This project does not ship a compiled .exe.
Users must build their own executable from the Python source.

1. Install Python (3.10+ recommended)

https://www.python.org/downloads/

Make sure "Add to PATH" is checked.

2. Install dependencies
From the project folder:

        pip install -r requirements.txt

3. Build the .exe
From the folder containing the script:

        pyinstaller --noconsole --onefile ytmusic_controller.py


After building, your .exe will be in:

dist/ytmusic_controller.exe

You can move this EXE anywhere.


* How to Use

- Starting the App: Double-click the .exe
- A small white-circle icon will appear in your system tray (near the clock)

* Default Hotkeys
Hotkey	Action
F2	    Chrome/YT Music volume down
F3	    Chrome/YT Music volume up
F7		Previous track
F8	    Play / pause
F9	    Next track

Works everywhere - even in fullscreen games.

* Tray Menu Options

Right-click the tray icon:
    1. Disable Hotkeys: 
        Turns off all global shortcuts.
        Useful if another app/game uses F2–F9.
        Click again to re-enable.
    2. Quit
        Stops the listener and closes the app completely.

* Notes

Controls Browser’s audio only - your system volume stays unchanged.
Use Chrome for YouTube Music.

Works on Windows 10 and 11.
