import tkinter as tk
from tkinter import ttk
from pystray import Icon, Menu, MenuItem
from PIL import Image


class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        # Hide the main window on close
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Create a tray icon
        self.icon = Icon("example", Image.open("icon.png"), "Example App")
        self.icon.menu = Menu(MenuItem("Exit", self.quit), MenuItem("Another entry", self.quit))
        self.icon.run()

    def on_close(self):
        # Hide the window instead of closing
        self.withdraw()
