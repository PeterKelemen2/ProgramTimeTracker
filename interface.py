import tkinter as tk

import custom_ui
import json_handler
import time_converter

ui = None
programs = json_handler.load_programs()

WIN_WIDTH = 700
WIN_HEIGHT = 600
BG = "#202331"
ACCENT = "#303754"
fallout3_icon = "icons/fallout3.png"


class App:
    def __init__(self):
        self.win = None
        self.create_window()
        self.create_container()
        self.create_entries()
        self.win.mainloop()

    def create_window(self):
        self.win = tk.Tk()
        self.win.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
        self.win.config(bg=BG)
        self.win.resizable(False, False)
        self.win.title("Program Time Tracker")
        self.win.protocol("WM_DELETE_WINDOW")

    def create_container(self):
        self.container = custom_ui.CustomLabelFrame(self.win, width=680, height=WIN_HEIGHT - 20, bg=BG, fill=ACCENT)
        self.container.canvas.place(x=10, y=10)

    def create_entries(self):
        self.entries = json_handler.load_programs()
        self.total_time = sum(entry['duration'] for entry in self.entries)
        custom_ui.total_time = self.total_time
        self.programs_list = []
        padding = 20
        entry_height = 100
        count = 0
        for entry in self.entries:
            self.programs_list.append(
                custom_ui.ProgramItem(self.container.canvas, width=640, height=entry_height, fill=ACCENT,
                                      name=entry["name"],
                                      duration=entry["duration"],
                                      icon_path=entry["icon_path"],
                                      last_duration=entry["last_duration"],
                                      count=entry["count"]))
            self.programs_list[-1].canvas.place(x=20, y=padding + count * (entry_height + padding))
            count += 1
