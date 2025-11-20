import os
from jproperties import Properties

CONFIG_FILE = "weather-app-settings.properties"

def load_window_size():
    p = Properties()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "rb") as f:
                p.load(f, "utf-8")

            width = p.get("width")
            height = p.get("height")

            if width and height:
                return f"{width.data}x{height.data}"
        except Exception:
            pass
    return "400x300"

def save_window_size(width, height):
    p = Properties()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "rb") as f:
                p.load(f, "utf-8")
        except Exception:
            pass

    p["width"] = str(width)
    p["height"] = str(height)

    try:
        with open(CONFIG_FILE, "wb") as f:
            p.store(f, encoding="utf-8")
    except Exception:
        pass
