import tkinter as tk
from tkinter import ttk
import custom_ui
import json_handler
import time_converter

ui = None
programs = json_handler.load_programs()

WIN_WIDTH = 700
WIN_HEIGHT = 700
BG = "#202331"
ACCENT = "#303754"
fallout3_icon = "icons/fallout3.png"


class App:
    def __init__(self):
        self.scrollable_frame = None
        self.round_container = None
        self.entries = None
        self.total_time = None
        self.programs = []
        self.scrollbar = None
        self.container = None
        self.scroll_canvas = None
        self.scroll_frame = None
        self.win = None
        self.create_window()
        self.create_scrollable_area()
        # self.create_entries()
        self.win.mainloop()

    def create_window(self):
        self.win = tk.Tk()
        self.win.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
        self.win.config(bg=BG)
        self.win.resizable(False, False)
        self.win.title("Program Time Tracker")
        self.win.protocol("WM_DELETE_WINDOW")

    def on_mousewheel(self, event):
        print("Scrolling")
        if event.num == 5 or event.delta == -120:
            if self.scroll_canvas.yview()[1] < 1.0:
                self.scroll_canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:
            if self.scroll_canvas.yview()[0] > 0.0:
                self.scroll_canvas.yview_scroll(-1, "units")

    def create_scrollable_area(self):
        style = ttk.Style()
        style.configure("Custom.TFrame", background=ACCENT)
        self.round_container = custom_ui.CustomLabelFrame(self.win, width=WIN_WIDTH - 20, height=WIN_HEIGHT - 100,
                                                          bg=BG,
                                                          fill=ACCENT)
        self.round_container.canvas.place(x=10, y=10)
        self.round_container.canvas.bind("<MouseWheel>", self.on_mousewheel)

        self.container = ttk.Frame(self.win, style="Custom.TFrame")
        self.scroll_canvas = tk.Canvas(self.container, width=WIN_WIDTH - 20, height=WIN_HEIGHT - 120,
                                       highlightthickness=0, bg=ACCENT)
        self.scrollbar = ttk.Scrollbar(self.container, orient=tk.VERTICAL, command=self.scroll_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.scroll_canvas, style="Custom.TFrame")
        self.scrollable_frame.bind("<Configure>",
                                   lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")))
        self.scroll_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scroll_canvas.config(yscrollcommand=self.scrollbar.set)

        self.scroll_canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", self.on_mousewheel)

        self.entries = json_handler.load_programs()
        self.total_time = sum(entry['duration'] for entry in self.entries)
        custom_ui.total_time = self.total_time
        self.programs_list = []
        padding = 20
        entry_height = 100
        count = 0
        for entry in self.entries:
            self.programs_list.append(
                custom_ui.ProgramItem(self.scrollable_frame, width=WIN_WIDTH - 40, height=entry_height, fill=ACCENT,
                                      name=entry["name"],
                                      duration=entry["duration"],
                                      icon_path=entry["icon_path"],
                                      last_duration=entry["last_duration"],
                                      count=entry["count"]))
            self.programs_list[-1].canvas.pack(pady=(0, 10))
            count += 1
            for elem in self.programs_list[-1].elem_list:
                elem.bind("<MouseWheel>", self.on_mousewheel)

        self.container.pack(padx=20, pady=20, fill="x")
        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.scrollbar.pack_forget()

    # def create_entries(self):
    #     self.entries = json_handler.load_programs()
    #     self.total_time = sum(entry['duration'] for entry in self.entries)
    #     custom_ui.total_time = self.total_time
    #     self.programs_list = []
    #     padding = 20
    #     entry_height = 100
    #     count = 0
    #     for entry in self.entries:
    #         self.programs_list.append(
    #             custom_ui.ProgramItem(self.scroll_frame, width=640, height=entry_height, fill=ACCENT,
    #                                   name=entry["name"],
    #                                   duration=entry["duration"],
    #                                   icon_path=entry["icon_path"],
    #                                   last_duration=entry["last_duration"],
    #                                   count=entry["count"]))
    #         self.programs_list[-1].canvas.place(x=10, y=padding + count * (entry_height + padding))
    #         self.programs_list[-1].canvas.bind("<MouseWheel>", self.on_mousewheel)
    #         count += 1
    #     self.scroll_frame.update_idletasks()
    #     self.scroll_canvas.config(scrollregion=self.scroll_canvas.bbox("all"))
