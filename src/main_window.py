import tkinter as tk

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):
        # Top section: Location
        # 100% wide (fill=tk.X), fixed height: 200
        self.location_frame = tk.LabelFrame(self.root, text="Location", height=100)
        self.location_frame.pack(side=tk.TOP, fill=tk.X)
        # pack_propagate(False) prevents the frame from shrinking to fit its (empty) content
        self.location_frame.pack_propagate(False)

        # Middle section: Current Weather
        # 100% wide (fill=tk.X), fixed height: 400
        self.weather_frame = tk.LabelFrame(self.root, text="Current Weather", height=200)
        self.weather_frame.pack(side=tk.TOP, fill=tk.X)
        self.weather_frame.pack_propagate(False)

        # Bottom section: Forecast
        # 100% wide and fills the rest of the window (fill=tk.BOTH, expand=True)
        self.forecast_frame = tk.LabelFrame(self.root, text="Forecast")
        self.forecast_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
