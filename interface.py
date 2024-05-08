import tkinter as tk

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
        self.scroll_canvas = None
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

    def on_mousewheel(self, event):
        print("Scrolling")
        if event.num == 5 or event.delta == -120:
            if self.scroll_canvas.yview()[1] < 1.0:
                self.scroll_canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:
            if self.scroll_canvas.yview()[0] > 0.0:
                self.scroll_canvas.yview_scroll(-1, "units")

    def create_container(self):
        # def on_mousewheel(event):
        #     if event.num == 5 or event.delta == -120:
        #         if self.history_scroll_canvas.yview()[1] < 1.0:
        #             self.history_scroll_canvas.yview_scroll(1, "units")
        #     elif event.num == 4 or event.delta == 120:
        #         if self.history_scroll_canvas.yview()[0] > 0.0:
        #             self.history_scroll_canvas.yview_scroll(-1, "units")

        self.container = custom_ui.CustomLabelFrame(self.win, width=WIN_WIDTH - 20, height=WIN_HEIGHT - 100, bg=BG,
                                                    fill=ACCENT)
        self.container.canvas.place(x=10, y=10)

        self.empty_label = tk.Label(self.container.canvas, width=1, height=1, bg=ACCENT, borderwidth=0)
        self.empty_label.place(x=10, y=10)

        self.scroll_canvas = tk.Canvas(self.empty_label, width=WIN_WIDTH - 40, height=WIN_HEIGHT - 120, bg="white",
                                       highlightthickness=0)

        self.scrollbar = tk.Scrollbar(self.empty_label, orient="vertical", command=self.scroll_canvas.yview, width=5)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.scrollbar.grid_forget()

        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scroll_canvas.grid(row=0, column=0, sticky="nsew")

        self.scroll_frame = tk.Frame(self.scroll_canvas, bg="black")
        self.scroll_canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.scroll_canvas.bind("<MouseWheel>", self.on_mousewheel)
        self.scroll_frame.bind("<MouseWheel>", self.on_mousewheel)
        self.scrollbar.bind("<MouseWheel>", self.on_mousewheel)

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
            # self.programs_list[-1].bind("<MouseWheel>", self.on_mousewheel)
            count += 1
        self.scroll_frame.update_idletasks()
        self.scroll_canvas.config(scrollregion=self.scroll_canvas.bbox("all"))
