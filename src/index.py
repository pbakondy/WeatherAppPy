import tkinter as tk
import os

from src.main_window import MainWindow
from src.settings import load_window_size, save_window_size

def main():
    root = tk.Tk()
    root.title("Weather App")
    root.geometry(load_window_size())
    root.config(padx=10, pady=10)

    icon_path = os.path.join("resources", "icons", "sun.png")
    if os.path.exists(icon_path):
        try:
            icon = tk.PhotoImage(file=icon_path)
            root.iconphoto(True, icon)
        except tk.TclError as e:
            print(f"Error loading icon: {e}")

    resize_timer = None

    def on_resize(event):
        nonlocal resize_timer
        if event.widget == root:
            if resize_timer:
                root.after_cancel(resize_timer)
            resize_timer = root.after(500, lambda: save_window_size(root.winfo_width(), root.winfo_height()))

    root.bind("<Configure>", on_resize)

    MainWindow(root)

    root.mainloop()
