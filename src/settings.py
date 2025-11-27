import os
from jproperties import Properties

class Settings:
    def __init__(self):
        self.CONFIG_FILE = "weather-app-settings.properties"

    def load_window_size(self):
        p = Properties()
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, "rb") as f:
                    p.load(f, "utf-8")

                width = p.get("width")
                height = p.get("height")

                if width and height:
                    return f"{width.data}x{height.data}"
            except Exception:
                pass
        return "600x600"

    def save_window_size(self, width, height):
        p = Properties()
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, "rb") as f:
                    p.load(f, "utf-8")
            except Exception:
                pass

        p["width"] = str(width)
        p["height"] = str(height)

        try:
            with open(self.CONFIG_FILE, "wb") as f:
                p.store(f, encoding="utf-8")
        except Exception:
            pass

    def load_location(self):
        p = Properties()
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, "rb") as f:
                    p.load(f, "utf-8")

                if p.get("name"):
                    return {
                        "name": p.get("name").data,
                        "country": p.get("country").data if p.get("country") else "",
                        "latitude": p.get("latitude").data if p.get("latitude") else "0.0",
                        "longitude": p.get("longitude").data if p.get("longitude") else "0.0",
                        "timezone": p.get("timezone").data if p.get("timezone") else "UTC"
                    }
            except Exception:
                pass
        return None

    def save_location(self, name, country, latitude, longitude, timezone):
        p = Properties()
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, "rb") as f:
                    p.load(f, "utf-8")
            except Exception:
                pass

        p["name"] = str(name)
        p["country"] = str(country)
        p["latitude"] = str(latitude)
        p["longitude"] = str(longitude)
        p["timezone"] = str(timezone)

        try:
            with open(self.CONFIG_FILE, "wb") as f:
                p.store(f, encoding="utf-8")
        except Exception:
            pass
