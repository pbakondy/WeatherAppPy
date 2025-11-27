import tkinter as tk
from tkinter import ttk
from src.restclient import RestClient
from src.settings import Settings

class Location(tk.Toplevel):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.rest_client = RestClient()
        self.title("Find Location")
        self.geometry("600x400")

        search_frame = tk.Frame(self)
        search_frame.pack(pady=10, fill="x", padx=10)

        tk.Label(search_frame, text="Location Name").pack(side="left")
        self.entry = tk.Entry(search_frame)
        self.entry.pack(side="left", padx=10, expand=True, fill="x")
        self.entry.bind("<Return>", lambda _: self.on_search(), "+")

        btn = tk.Button(search_frame, text="Search", command=self.on_search)
        btn.pack(side="left")

        results_frame = tk.Frame(self)
        results_frame.pack(pady=10, padx=10, fill="both", expand=True)

        columns = ("Name", "Country", "Latitude", "Longitude", "Timezone")
        self.tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=10)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        bottom_frame = tk.Frame(self)
        bottom_frame.pack(pady=10)

        tk.Button(bottom_frame, text="Set Location", command=self.on_set_location).pack(side="left", padx=10)
        tk.Button(bottom_frame, text="Close", command=self.destroy).pack(side="left", padx=10)

    def on_search(self):
        city = self.entry.get()
        print(f"Searching for: {city}")

        if not city:
            return

        locations = self.rest_client.fetchGeocoding(city)

        for item in self.tree.get_children():
            self.tree.delete(item)

        if locations and "results" in locations:
            for loc in locations["results"]:
                values = (
                    loc.get("name", "N/A"),
                    loc.get("country", "N/A"),
                    loc.get("latitude", "N/A"),
                    loc.get("longitude", "N/A"),
                    loc.get("timezone", "N/A")
                )
                self.tree.insert("", "end", values=values)

    def on_set_location(self):
        selected_item = self.tree.selection()
        if not selected_item:
            return

        item = self.tree.item(selected_item[0])
        values = item['values']

        if values:
            name, country, lat, lon, timezone = values

            settings = Settings()
            settings.save_location(name, country, lat, lon, timezone)

            if self.main_window:
                self.main_window.update_location_ui(name, country, lat, lon, timezone)

            self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = Location(root)
    tk.mainloop()
