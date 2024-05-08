import tkinter as tk

import custom_ui
import json_handler
import time_converter

ui = None
programs = json_handler.load_programs()

WIN_WIDTH = 620
WIN_HEIGHT = 600
BG = "#202331"
ACCENT = "#303754"


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
        self.container = custom_ui.CustomLabelFrame(self.win, width=600, height=200, bg=BG, fill=ACCENT)
        self.container.canvas.place(x=10, y=10)

    def create_entries(self):
        self.entries = json_handler.load_programs()
        self.programs_list = []
        for entry in self.entries:
            self.programs_list.append(
                custom_ui.ProgramItem(self.container.canvas, width=560, height=100, fill=ACCENT,
                                      name=entry["name"],
                                      duration=entry["duration"],
                                      last_duration=entry["last_duration"],
                                      count=entry["count"]))
            self.programs_list[-1].canvas.place(x=20, y=20)
