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
        self.entries = None
        self.total_time = None
        self.programs = []
        self.scrollbar = None
        self.container = None
        self.scroll_canvas = None
        self.scroll_frame = None
        self.win = None
        self.create_window()
        self.create_container()
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

    def on_canvas_configure(self, event):
        # Update the canvas scroll region
        self.scroll_canvas.config(scrollregion=self.scroll_canvas.bbox("all"))

    def create_container(self):
        self.round_container = custom_ui.CustomLabelFrame(self.win, width=WIN_WIDTH - 20, height=WIN_HEIGHT - 100,
                                                          bg=BG,
                                                          fill=ACCENT)
        self.round_container.canvas.place(x=10, y=10)

        self.container = ttk.Frame(self.container)
        self.scroll_canvas = tk.Canvas(self.container, width=WIN_WIDTH - 20, height=WIN_HEIGHT - 120,
                                       highlightthickness=0, bg=ACCENT)
        self.scrollbar = ttk.Scrollbar(self.container, orient=tk.VERTICAL, command=self.scroll_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.scroll_canvas)
        self.scrollable_frame.bind("<Configure>",
                                   lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")))
        self.scroll_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.scroll_canvas.config(yscrollcommand=self.scrollbar.set)

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
            self.programs_list[-1].canvas.pack(padx=10, pady=(0, 10))
            count += 1

        self.container.pack(pady=20, fill="x")
        self.scroll_canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # self.entries = json_handler.load_programs()
        # self.total_time = sum(entry['duration'] for entry in self.entries)
        # custom_ui.total_time = self.total_time
        # self.programs_list = []
        # padding = 20
        # entry_height = 100
        # count = 0
        # for entry in self.entries:
        #     self.programs_list.append(
        #         custom_ui.ProgramItem(self.scroll_frame, width=WIN_WIDTH - 40, height=entry_height, fill=ACCENT,
        #                               name=entry["name"],
        #                               duration=entry["duration"],
        #                               icon_path=entry["icon_path"],
        #                               last_duration=entry["last_duration"],
        #                               count=entry["count"]))
        #     self.programs_list[-1].canvas.place(x=0, y=count * (entry_height + padding))
        #     self.programs_list[-1].canvas.bind("<MouseWheel>", self.on_mousewheel)
        #     for elem in self.programs_list[-1].elem_list:
        #         elem.bind("<MouseWheel>", self.on_mousewheel)
        #     count += 1
        # self.scroll_frame.update_idletasks()
        # self.scroll_canvas.config(scrollregion=self.scroll_canvas.bbox("all"))

        # Create container frame
        # self.container = custom_ui.CustomLabelFrame(self.win, width=WIN_WIDTH - 20, height=WIN_HEIGHT - 100, bg=BG,
        #                                             fill=ACCENT)
        # self.container.canvas.place(x=10, y=10)

        # Create canvas for scrolling
        # self.scroll_canvas = tk.Canvas(self.container.canvas, width=WIN_WIDTH - 40, height=WIN_HEIGHT - 120, bg="white",
        #                                highlightthickness=0)
        # self.scroll_canvas.pack(padx=10, pady=10, side="left", fill="both", expand=True)
        #
        # # Create scrollbar
        # self.scrollbar = tk.Scrollbar(self.container.canvas, orient="vertical", command=self.scroll_canvas.yview,
        #                               width=5)
        # self.scrollbar.pack(side="right", fill="y")
        #
        # # Configure canvas scrolling
        # self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)
        #
        # # Create scrollable frame
        # self.scroll_frame = tk.Frame(self.scroll_canvas, bg="black")
        # self.scroll_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        #
        # # Bind mouse wheel event
        # self.scroll_canvas.bind("<MouseWheel>", self.on_mousewheel)

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
                custom_ui.ProgramItem(self.scroll_frame, width=640, height=entry_height, fill=ACCENT,
                                      name=entry["name"],
                                      duration=entry["duration"],
                                      icon_path=entry["icon_path"],
                                      last_duration=entry["last_duration"],
                                      count=entry["count"]))
            self.programs_list[-1].canvas.place(x=10, y=padding + count * (entry_height + padding))
            self.programs_list[-1].canvas.bind("<MouseWheel>", self.on_mousewheel)
            count += 1
        self.scroll_frame.update_idletasks()
        self.scroll_canvas.config(scrollregion=self.scroll_canvas.bbox("all"))
