# Weather Application

Peter Bakondy (NUVOYP)

## Application Description

This application will display the weather forecast and current weather for a given location.
It uses open-meteo.com API to get geolocation and weather data.

## Modules and Functions

### BpMainWindow

It draws the main window and displays the weather forecast and current weather data.
It uses `tkinter` to draw the GUI.
It uses package `pandas` for data processing.
BpMainWindow uses `Setting` to load Location data.
BpMainWindow uses `RestClient` to get weather data.

List of functions: `setup_ui`, `open_location_window`, `update_location_ui`, `load_initial_location`, `refresh_weather`, `bp_draw_current`, `bp_draw_daily`

List of static functions: `degrees_to_direction`, `get_weather_description`

## Classes

### Location

It is a search interface to location data.
The user can enter a location name, it displays search results in a table, then the user is able to select the wanted location.
It uses package `RestClient` to fetch Geolocation and `Setting` to save selected location settings.

List of functions: `on_search`, `on_set_location`

### Setting

Loads and saves location settings and main window sizes to a properties file.
It uses package `properties`.

List of functions: `load_window_size`, `save_window_size`, `load_location`, `save_location`

### RestClient

HTTP communication with open-meteo.com.
It uses packages `openmeteo_requests` and `requests`.

List of functions: `fetchGeocoding`, `fetchForecast`
