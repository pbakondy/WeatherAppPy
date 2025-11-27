import openmeteo_requests
import requests

class RestClient:
    def __init__(self):
        self.geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"
        self.forecast_url = "https://api.open-meteo.com/v1/forecast"
        self.openmeteo = openmeteo_requests.Client()
        self.params = {
            "daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "precipitation_sum",
                      "precipitation_probability_max", "wind_speed_10m_max", "wind_direction_10m_dominant"],
            "current": ["temperature_2m", "apparent_temperature", "precipitation", "weather_code", "wind_speed_10m",
                        "wind_direction_10m", "pressure_msl"],
            "timezone": "auto",
        }

    def fetchGeocoding(self, name: str):
        return requests.get(self.geocoding_url, params={"name":name}).json()

    def fetchForecast(self, coords: tuple):
        params = self.params.copy()
        params.update({"latitude": coords[0], "longitude": coords[1]})
        return self.openmeteo.weather_api(self.forecast_url, params=params)

