import tkinter as tk
import math
from tkinter import ttk
import pandas as pd

from src.location import Location
from src.settings import Settings
from src.restclient import RestClient


def degrees_to_direction(degrees):
    directions = [
        "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
    ]
    index = round(degrees / (360. / 16.)) % 16
    return directions[index]


def get_weather_description(code):
    code = int(code)
    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light Drizzle",
        53: "Moderate Drizzle",
        55: "Dense Drizzle",
        56: "Light Freezing Drizzle",
        57: "Dense Freezing Drizzle",
        61: "Slight Rain",
        63: "Moderate Rain",
        65: "Heavy Rain",
        66: "Light Freezing Rain",
        67: "Heavy Freezing Rain",
        71: "Slight Snow Fall",
        73: "Moderate Snow Fall",
        75: "Heavy Snow Fall",
        77: "Snow grains",
        80: "Slight Rain Showers",
        81: "Moderate Rain Showers",
        82: "Violent Rain Showers",
        85: "Slight Snow Showers",
        86: "Heavy Snow Showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    return descriptions.get(code, f"Unknown code ({code})")


class BpMainWindow:
    def __init__(self, root):
        self.forecast_frame = None
        self.weather_frame = None
        self.btn_set_location = None
        self.lbl_location_coords = None
        self.lbl_location_name = None
        self.location_frame = None
        self.root = root
        self.settings = Settings()
        self.rest_client = RestClient()
        self.setup_ui()
        self.load_initial_location()

    def setup_ui(self):
        self.location_frame = tk.LabelFrame(self.root, text="Location", height=80)
        self.location_frame.pack(side="top", fill="x")
        self.location_frame.pack_propagate(False)

        self.lbl_location_name = tk.Label(self.location_frame, text="No location set", font=("Arial", 12, "bold"))
        self.lbl_location_name.pack(side="left", padx=10, pady=10)

        self.lbl_location_coords = tk.Label(self.location_frame, text="", font=("Arial", 10))
        self.lbl_location_coords.pack(side="left", padx=10, pady=10)

        self.btn_set_location = tk.Button(self.location_frame, text="Set location", command=self.open_location_window, padx=10, pady=5, font=("Arial", 10))
        self.btn_set_location.pack(side="right", padx=10, pady=10)

        self.weather_frame = tk.LabelFrame(self.root, text="Current Weather", height=200)
        self.weather_frame.pack(side="top", fill="x")
        self.weather_frame.pack_propagate(False)
        self.weather_frame.columnconfigure(0, weight=1)
        self.weather_frame.columnconfigure(1, weight=1)

        self.forecast_frame = tk.LabelFrame(self.root, text="Forecast")
        self.forecast_frame.pack(side="top", fill="both", expand=True)

    def open_location_window(self):
        Location(self.root, self)

    def update_location_ui(self, name, country, lat, lon, timezone):
        self.lbl_location_name.config(text=f"{name}, {country}")
        self.lbl_location_coords.config(text=f"({lat}, {lon})\nTimezone: {timezone}")
        self.refresh_weather((float(lat), float(lon)))

    def load_initial_location(self):
        loc = self.settings.load_location()
        if loc:
            self.update_location_ui(loc['name'], loc['country'], loc['latitude'], loc['longitude'], loc['timezone'])

    def refresh_weather(self, coords):
        try:
            forecast_data = self.rest_client.fetchForecast(coords)
            if forecast_data:
                if isinstance(forecast_data, list):
                    weather = forecast_data[0]
                else:
                    weather = forecast_data

                current = weather.Current()
                daily = weather.Daily()

                self.bp_draw_current(current)
                self.bp_draw_daily(daily)

        except Exception as e:
            print(f"Error fetching weather: {e}")


    def bp_draw_current(self, current):

        def get_current_val(idx):
            return current.Variables(idx).Value()

        temp = get_current_val(0)
        app_temp = get_current_val(1)
        precip = get_current_val(2)
        w_code = get_current_val(3)
        weather_desc = get_weather_description(w_code)
        wind_spd = get_current_val(4)
        wind_dir = get_current_val(5)
        pressure = get_current_val(6)

        wind_dir_str = degrees_to_direction(wind_dir)

        for widget in self.weather_frame.winfo_children():
            widget.destroy()

        tk.Label(self.weather_frame, text=f"Temperature: {temp:.1f}°C").grid(row=0, column=0, sticky="w", padx=10,
                                                                             pady=1)
        tk.Label(self.weather_frame, text=f"Apparent Temp: {app_temp:.1f}°C").grid(row=1, column=0, sticky="w", padx=10,
                                                                                   pady=1)
        tk.Label(self.weather_frame, text=f"Precipitation: {precip} mm").grid(row=2, column=0, sticky="w", padx=10,
                                                                              pady=1)
        tk.Label(self.weather_frame, text=f"Weather: {weather_desc}").grid(row=3, column=0, sticky="w", padx=10,
                                                                               pady=1)
        tk.Label(self.weather_frame, text=f"Pressure: {pressure:.1f} hPa").grid(row=0, column=1, sticky="w", padx=10,
                                                                                pady=1)
        tk.Label(self.weather_frame, text=f"Wind Speed: {wind_spd:.1f} km/h").grid(row=1, column=1, sticky="w", padx=10,
                                                                                   pady=1)

        wind_frame = tk.Frame(self.weather_frame)
        wind_frame.grid(row=2, column=1, sticky="w", padx=10, pady=1)

        tk.Label(wind_frame, text=f"Wind Direction: {wind_dir_str} ({wind_dir:.1f}°)").pack(side="left")

        canvas = tk.Canvas(wind_frame, width=20, height=20, highlightthickness=0)
        canvas.pack(side="left", padx=5)
        cx, cy = 10, 10
        length = 8
        angle_rad = math.radians(wind_dir - 90 + 180)
        x1 = cx + length * math.cos(angle_rad)
        y1 = cy + length * math.sin(angle_rad)
        x2 = cx - length * math.cos(angle_rad)
        y2 = cy - length * math.sin(angle_rad)
        canvas.create_line(x2, y2, x1, y1, arrow="last", width=2)

    def bp_draw_daily(self, daily):
        for widget in self.forecast_frame.winfo_children():
            widget.destroy()

        columns = ("Date", "Weather", "Max Temp", "Min Temp", "Precipitation", "Precip Prob", "Max Wind Speed",
                   "Wind Direction")
        tree = ttk.Treeview(self.forecast_frame, columns=columns, show="headings", height=7)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        tree.pack(fill="both", expand=True)

        daily_data = {"date": pd.date_range(
            start=pd.to_datetime(daily.Time(), unit="s", utc=True),
            end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
            freq=pd.Timedelta(seconds=daily.Interval()),
            inclusive="left"
        ), "weather_code": daily.Variables(0).ValuesAsNumpy(), "temperature_2m_max": daily.Variables(1).ValuesAsNumpy(),
            "temperature_2m_min": daily.Variables(2).ValuesAsNumpy(),
            "precipitation_sum": daily.Variables(3).ValuesAsNumpy(),
            "precipitation_probability_max": daily.Variables(4).ValuesAsNumpy(),
            "wind_speed_10m_max": daily.Variables(5).ValuesAsNumpy(),
            "wind_direction_10m_dominant": daily.Variables(6).ValuesAsNumpy()}

        df = pd.DataFrame(data=daily_data)

        for i in range(len(df)):
            row = df.iloc[i]
            date_str = row["date"].strftime("%Y-%m-%d")
            w_code = get_weather_description(int(row["weather_code"]))
            max_temp = f"{row['temperature_2m_max']:.1f}°C"
            min_temp = f"{row['temperature_2m_min']:.1f}°C"
            precip = f"{row['precipitation_sum']:.1f} mm"
            precip_prob = f"{int(row['precipitation_probability_max'])}%"
            wind_spd = f"{row['wind_speed_10m_max']:.1f} km/h"
            wind_dir_val = row['wind_direction_10m_dominant']
            wind_dir = f"{degrees_to_direction(wind_dir_val)} ({int(wind_dir_val)}°)"

            tree.insert("", "end",
                        values=(date_str, w_code, max_temp, min_temp, precip, precip_prob, wind_spd, wind_dir))
