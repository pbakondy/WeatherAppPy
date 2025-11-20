import tkinter as tk
import os

def main():
    root = tk.Tk()
    root.title("Weather App")
    root.geometry("400x300")

    icon_path = os.path.join("resources", "icons", "sun.png")
    if os.path.exists(icon_path):
        icon = tk.PhotoImage(file=icon_path)
        root.iconphoto(True, icon)

    root.mainloop()

if __name__ == "__main__":
    main()