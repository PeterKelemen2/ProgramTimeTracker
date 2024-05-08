import os
import time
import tkinter
from tkinter import PhotoImage, Canvas

import PIL.ImageOps
from PIL import Image, ImageTk

import custom_button
import interface
import main
import time_converter

# import debug
# import interface

bg_path = "assets/rounded_frame.png"
circle = "assets/frame_circle.png"
rect = "assets/frame_square.png"
toggled_on = "assets/toggle_button/toggle_on.png"
toggled_off = "assets/toggle_button/toggle_off.png"
no_photo_path = "assets/no_photo_small.jpg"

ACCENT = "#3a3a3a"
BGCOLOR = "#3a3a3a"
WHITE = "#ffffff"
BLACK = "#000000"

DARK_FONT_COLOR = "#ffffff"
LIGHT_FONT_COLOR = "#000000"
FONT_COLOR = "#ffffff"
TIME_FONT_SIZE = 12
BIG_FONT_SIZE = 14
FONT = ("Ubuntu", TIME_FONT_SIZE)
BOLD_FONT = ("Ubuntu", TIME_FONT_SIZE, "bold")
BIG_FONT = ("Ubuntu", BIG_FONT_SIZE)
BIG_FONT_BOLD = ("Ubuntu", BIG_FONT_SIZE, "bold")

PROGRAM_ITEM_PLACEMENT = [0, 10, 80, 270, 420, 560]
total_time = 0
fallout3_icon = "icons/fallout3.png"

ui: interface = None


def set_interface_instance(inter):
    global ui
    ui = inter


class ProgramItem:
    def __init__(self, master, width, height, bg=None, fill=None, icon_path=None, name=None, duration=None,
                 last_duration=None, count=None):
        self.master = master
        self.width = width
        self.height = height
        if bg is None:
            self.bg = interface.BG
        else:
            self.bg = bg
        self.fill = fill

        self.icon_photo = icon_path
        self.name = name
        self.duration = duration
        self.duration_hours = time_converter.convert_seconds(self.duration)
        self.last_duration = last_duration
        self.last_duration_hours = time_converter.convert_seconds(self.last_duration)
        self.count = count

        # total_dur = 10000
        duration_width = 110
        self.duration_percent = (duration * 100) // total_time
        self.last_duration_percent = (last_duration * 100) // duration

        self.canvas = Canvas(self.master, width=self.width, height=self.height, bg=self.bg, highlightthickness=0)
        self.canvas.pack()

        self.container = CustomLabelFrame(self.canvas, width=self.width, height=self.height, bg=interface.ACCENT,
                                          fill=interface.BG)
        self.container.canvas.place(x=0, y=0)

        self.text_list = []
        self.unit_list = []

        # self.icon_img = Image.open(fallout3_icon)
        self.icon_photo = ImageTk.PhotoImage(PIL.Image.open(icon_path).resize((50, 50)))
        self.icon_label = tkinter.Label(self.container.canvas, bg=self.bg, image=self.icon_photo)
        self.unit_list.append(self.icon_label)
        # self.icon_label.place(x=10, y=30)

        self.text_list = []
        self.name_title = tkinter.Label(self.container.canvas, text="Name", font=BOLD_FONT, bg=self.bg, fg="white")
        self.name_text = tkinter.Label(self.container.canvas, text=self.name, bg=self.bg, font=FONT, fg="white")
        self.unit_list.append([self.name_title, self.name_text])

        self.duration_title = tkinter.Label(self.container.canvas, text="Total duration", bg=self.bg, font=BOLD_FONT,
                                            fg="white")
        self.duration_text = tkinter.Label(self.container.canvas, text=self.duration_hours, bg=self.bg, font=FONT,
                                           fg="white")
        self.duration_pb = CustomProgressBar(self.container.canvas, width=duration_width, height=22, padding=4,
                                             radius=8,
                                             bg=self.bg, bar_bg_accent="#6AB187", pr_bar="#73ff7b")
        self.duration_pb.set_percentage(self.duration_percent)
        # self.duration_pb.canvas.place(x=169, y=65)
        self.unit_list.append([self.duration_title, self.duration_text, self.duration_pb])

        self.last_duration_title = tkinter.Label(self.container.canvas, text="Last duration", bg=self.bg,
                                                 font=BOLD_FONT, fg="white")
        self.last_duration_text = tkinter.Label(self.container.canvas, text=self.last_duration_hours, bg=self.bg,
                                                font=FONT,
                                                fg="white")
        self.text_list.append(self.last_duration_text)
        self.last_duration_pb = CustomProgressBar(self.container.canvas, width=duration_width, height=22, padding=4,
                                                  radius=8, bg=self.bg, bar_bg_accent="#6AB187", pr_bar="#73ff7b")
        self.last_duration_pb.set_percentage(self.last_duration_percent)
        # self.last_duration_pb.canvas.place(x=297, y=65)
        self.unit_list.append([self.last_duration_title, self.last_duration_text, self.last_duration_pb])
        # self.last_duration_text.place(x=self.duration_text.winfo_reqwidth() + 10, y=self.height // 2)

        self.count_title = tkinter.Label(self.container.canvas, text="Count", bg=self.bg, font=BOLD_FONT, fg="white")
        self.count_text = tkinter.Label(self.container.canvas, text=self.count, bg=self.bg, font=FONT, fg="white")
        self.unit_list.append([self.count_title, self.count_text])
        # self.count_text.place(x=self.last_duration_text.winfo_reqwidth() + 10, y=self.height // 2)

        self.icon_label.place(x=10, y=25)

        item = 1
        # print(self.unit_list)
        for unit in self.unit_list:
            y_to_place = 15

            if type(unit) == list:
                for elem in unit:
                    # item = 1
                    elem.place(x=PROGRAM_ITEM_PLACEMENT[item], y=y_to_place)
                    y_to_place += 25
            else:
                unit.place(x=PROGRAM_ITEM_PLACEMENT[item], y=y_to_place)

            item += 1


# noinspection PyUnresolvedReferences
class CardItem:
    def __init__(self, master, width, height, bg=BLACK, title="", img_path=None, video_path=None,
                 result=None, norm=None, stab=None):
        self.diff_text = None
        self.diff_title = None
        self.path_text = None
        self.norm = norm
        self.stab = stab
        self.result = result
        self.text = None
        self.custom_path = video_path
        self.video_path = video_path
        self.width = width
        self.height = height
        self.bg = bg
        self.title = title
        self.image_padding = 20
        self.canvas = Canvas(master, width=self.width, height=self.height, bg=interface.BGCOLOR, highlightthickness=0)
        self.canvas.pack()
        self.stab_text_to_show = ui.lang["no_data"]
        self.norm_text_to_show = ui.lang["no_data"]
        self.container = CustomLabelFrame(self.canvas, width=self.width, height=self.height, text=self.title,
                                          bg=interface.BGCOLOR, fill=interface.ACCENT)
        self.container.canvas.place(x=0, y=0)

        self.photo = ImageTk.PhotoImage(self.create_photo(img_path))
        self.photo_label = (tkinter.Label(self.container.canvas, image=self.photo, bg=interface.FONT_COLOR))
        self.photo_label.place(x=self.image_padding, y=self.image_padding)

        self.create_text(video_path, result, self.stab, self.norm)

        self.process_button = custom_button.CustomButton(self.container.canvas, text=ui.lang["load_video"],
                                                         bg=interface.ACCENT,
                                                         button_type=custom_button.wide_button, command=self.load_video)
        self.process_button.canvas.place(
            x=self.width - self.process_button.canvas.winfo_reqwidth() - self.container.get_radius() * 2,
            y=self.height - self.process_button.canvas.winfo_reqheight() - self.container.get_radius() * 2)

    def load_video(self):
        global ui
        if ui is not None:
            ui.set_selected_file_path(self.video_path)
            ui.create_stabilization_progress_bar()
            ui.create_processing_progress_bar()
            ui.set_main_focus()

    def create_photo(self, img_path=None):
        if img_path is None or not os.path.exists(img_path):
            image = Image.open(no_photo_path)
        else:
            image = Image.open(img_path)
        width, height = image.size
        new_height = self.container.get_height() - 50
        aspect_ratio = new_height / height
        new_width = int(width * aspect_ratio)

        image = image.resize((new_width, new_height), Image.BILINEAR)

        self.image_padding = (self.container.get_height() - new_height) // 2
        return image

    def create_text(self, path=None, result="", stab=None, norm=None):
        self.path_text, self.text, self.diff_text, self.diff_title = None, None, None, None
        title_x = self.photo.width() + self.image_padding * 2
        self.path_text = tkinter.Label(self.container.canvas, text=ui.lang["path"], font=BOLD_FONT,
                                       fg=interface.FONT_COLOR,
                                       bg=interface.ACCENT)
        self.path_text.place(x=title_x, y=self.image_padding)
        text = ""
        if path is None or not os.path.exists(path):
            text = ui.lang["no_path"]
        else:
            text = path
        self.text = tkinter.Label(self.container.canvas,
                                  text=text,
                                  justify="left",
                                  font=FONT,
                                  wraplength=self.width - self.image_padding * 3 - self.photo.width() - self.path_text.winfo_reqwidth(),
                                  fg=interface.FONT_COLOR,
                                  bg=interface.ACCENT)
        text_x = self.photo.width() + self.image_padding * 2 + self.path_text.winfo_reqwidth()
        self.text.place(x=text_x, y=self.image_padding)

        self.diff_title = tkinter.Label(self.container.canvas, text=ui.lang["result"], font=BOLD_FONT,
                                        fg=interface.FONT_COLOR,
                                        bg=interface.ACCENT)

        # Binding y coordinate to self.text in case it becomes more lines than one
        self.diff_title.place(x=title_x, y=self.image_padding + self.text.winfo_reqheight())
        self.diff_text = tkinter.Label(self.container.canvas, text=result, font=FONT,
                                       fg=interface.FONT_COLOR, bg=interface.ACCENT)
        self.diff_text.place(x=self.photo.width() + self.image_padding * 2 + self.diff_title.winfo_reqwidth(),
                             y=self.image_padding + self.text.winfo_reqheight())

        if self.norm is False:
            self.norm_text_to_show = ui.lang["no"]
        elif self.norm is True:
            self.norm_text_to_show = ui.lang["yes"]

        self.norm_title = tkinter.Label(self.container.canvas, text=ui.lang["norm"], font=BOLD_FONT,
                                        fg=interface.FONT_COLOR, bg=interface.ACCENT)
        self.norm_text = tkinter.Label(self.container.canvas, text=self.norm_text_to_show, font=FONT,
                                       fg=interface.FONT_COLOR, bg=interface.ACCENT)
        self.norm_title.place(x=title_x, y=self.image_padding * 2 + self.text.winfo_reqheight())
        self.norm_text.place(x=self.photo.width() + self.image_padding * 2 + self.norm_title.winfo_reqwidth(),
                             y=self.image_padding * 2 + self.text.winfo_reqheight())

        if self.stab is True:
            self.stab_text_to_show = ui.lang["yes"]

        if self.stab is False:
            self.stab_text_to_show = ui.lang["no"]
        self.stab_title = tkinter.Label(self.container.canvas, text=ui.lang["stab"], font=BOLD_FONT,
                                        fg=interface.FONT_COLOR, bg=interface.ACCENT)
        self.stab_text = tkinter.Label(self.container.canvas, text=self.stab_text_to_show, font=FONT,
                                       fg=interface.FONT_COLOR, bg=interface.ACCENT)
        self.stab_title.place(x=title_x, y=self.image_padding * 3 + self.text.winfo_reqheight())
        self.stab_text.place(x=self.photo.width() + self.image_padding * 2 + self.stab_title.winfo_reqwidth(),
                             y=self.image_padding * 3 + self.text.winfo_reqheight())


class CustomToggleButton:
    def __init__(self, master, width, height, text="", state=True, bg=None):
        self.width = width
        self.height = height
        self.bg = bg
        self.text = text
        self.disabled = False
        self.state = state
        self.text_item = None

        self.toggled_on_im_file = Image.open(toggled_on).convert("RGBA")
        self.toggled_off_im_file = Image.open(toggled_off).convert("RGBA")

        self.canvas = Canvas(master, width=self.width, height=self.height, bg=self.bg, highlightthickness=0)
        self.canvas.pack()

        self.t_on_im = self.toggled_on_im_file.resize((self.width, self.height))
        self.t_off_im = self.toggled_off_im_file.resize((self.width, self.height))

        self.toggled_on_image = ImageTk.PhotoImage(self.t_on_im)
        self.toggled_off_image = ImageTk.PhotoImage(self.t_off_im)

        self.text_item = tkinter.Label(self.canvas, text=self.text, height=0, anchor="center", fg=interface.FONT_COLOR,
                                       font=FONT,
                                       bg=interface.ACCENT)
        self.canvas.config(width=self.width + self.text_item.winfo_reqwidth() + 20)
        self.text_item.place(x=self.width + 10, y=5)

        if self.state:
            self.image_item = self.canvas.create_image(self.width // 2, self.height // 2, anchor="center",
                                                       image=self.toggled_on_image)
        else:
            self.image_item = self.canvas.create_image(self.width // 2, self.height // 2, anchor="center",
                                                       image=self.toggled_off_image)

        self.canvas.bind("<Button-1>", self.toggle)
        self.text_item.bind("<Button-1>", self.toggle)

    def toggle(self, event=None):
        if not self.disabled:
            self.state = not self.state
            self.canvas.delete(self.image_item)
            if self.state:
                self.image_item = self.canvas.create_image(self.width // 2, self.height // 2, anchor="center",
                                                           image=self.toggled_on_image)
            else:
                self.image_item = None
                self.image_item = self.canvas.create_image(self.width // 2, self.height // 2, anchor="center",
                                                           image=self.toggled_off_image)

    def disable(self):
        self.disabled = True

    def enable(self):
        self.disabled = False

    def get_state(self):
        return self.state

    def config(self, bg=None, fg=None, text=None):
        if bg is not None:
            self.canvas.config(bg=bg)
            if fg is not None and self.text is not None:
                self.text_item.config(bg=bg, fg=fg)
        if fg is not None and text is not None:
            self.text_item.config(fg=fg)
        if text is not None:
            self.text_item.config(text=text)
            self.text = text


class CustomLabelFrame:
    def __init__(self, master, width, height, text="", fill=BLACK, fg=WHITE, bg=BGCOLOR, radius=10):
        self.width = width
        self.height = height
        self.fill = fill
        self.fg = fg
        self.bg = bg
        self.text = text
        self.radius = radius
        self.canvas = Canvas(master, width=width, height=height, bg=bg, highlightthickness=0)
        self.canvas.pack()

        self.item_list = list()
        self.rect_im = None
        self.circle_im = None
        self.rect_im_hor = None
        self.overlay = None
        self.rect_im_ver = None
        self.text_item = None
        self.center = None
        self.cir_im = None
        self.rec_im_hor = None
        self.rec_im_ver = None
        self.center_rec = None

        self.create_images()
        self.create_labelframe()

    def load_images(self):
        # Load the images using PIL
        self.circle_im = None
        self.rect_im = None
        self.circle_im = Image.open(circle).convert("RGBA")
        self.rect_im = Image.open(rect).convert("RGBA")

    def create_images(self):
        """
        Creates images for circle and rectangle shapes.

        This method loads the images for circle and rectangle shapes, composites them with a specified overlay color,
        and resizes them to the desired dimensions. The circle image is resized to twice the radius for both width and
        height. The rectangle images are resized to match the canvas dimensions, with adjustments made for the circle's
        presence.

        Returns:
            None
        """
        self.load_images()

        self.overlay = Image.new("RGBA", self.circle_im.size, self.fill)
        self.circle_im = Image.composite(self.overlay, self.circle_im, self.circle_im)
        self.rect_im = Image.composite(self.overlay, self.rect_im, self.rect_im)

        # Resize the image (width, height)
        self.circle_im = self.circle_im.resize((self.radius * 2, self.radius * 2))
        self.rect_im_hor = self.rect_im.resize((self.width, self.height - self.radius * 2))
        self.rect_im_ver = self.rect_im.resize((self.width - self.radius * 2, self.height))

    def create_labelframe(self):
        """
        Creates a label frame on the canvas with circle and rectangle images along with text.

        This method creates a label frame on the canvas and populates it with circle and rectangle images
        along with text. The circle images are positioned at four corners of the canvas, while the rectangle
        images are positioned at the center of the canvas. Text is added at a specified position
        with the given fill color, anchor point, and font.

        Note:
            Ensure that the `circle_im`, `rect_im_hor`, and `rect_im_ver` attributes are set with the appropriate
            image files before calling this method.

        Returns:
            None
        """
        self.item_list = list()
        self.cir_im = ImageTk.PhotoImage(self.circle_im)
        self.rec_im_hor = ImageTk.PhotoImage(self.rect_im_hor)
        self.rec_im_ver = ImageTk.PhotoImage(self.rect_im_ver)

        # Creating circles (x,y)
        self.item_list.append(self.canvas.create_image(self.radius, self.radius, anchor="center", image=self.cir_im))
        self.item_list.append(
            self.canvas.create_image(self.width - self.radius, self.radius, anchor="center", image=self.cir_im))
        self.item_list.append(
            self.canvas.create_image(self.radius, self.height - self.radius, anchor="center", image=self.cir_im))
        self.item_list.append(
            self.canvas.create_image(self.width - self.radius, self.height - self.radius, anchor="center",
                                     image=self.cir_im))

        # Creating rectangles
        self.item_list.append(self.canvas.create_image(self.width // 2, self.height // 2, image=self.rec_im_hor))
        self.item_list.append(
            self.canvas.create_image(self.radius, self.height // 2, anchor="w", image=self.rec_im_ver))

        self.text_item = self.canvas.create_text(self.radius, self.radius, text=self.text, fill=self.fg, anchor="w",
                                                 font=BOLD_FONT)

    def config(self, text=None, fg=None, bg=None, fill=None):
        if text is not None:
            self.text = text
            self.canvas.itemconfig(self.text_item, text=self.text)
        if fg is not None:
            self.fg = fg
            self.canvas.itemconfig(self.text_item, fill=self.fg)
        if bg is not None:
            self.bg = bg
            self.canvas.config(bg=self.bg)
        if fill is not None:
            self.change_fill_color(fill)

    def change_width(self, new_width):
        pass

    def switch_theme(self, new_fill=None, new_text_color=None, new_bg=None, buttons=None, labels=None):
        """
        Switches the theme of the user interface.

        Args:
            new_fill (str): The new fill color for elements like buttons.
            new_text_color (str): The new text color for elements like buttons and labels.
            new_bg (str): The new background color for the canvas.
            buttons (list): A list of button widgets to apply the new fill color.
            labels (list): A list of label widgets to apply the new fill and text colors.
        """
        if new_fill is not None: self.change_fill_color(new_fill)
        if new_text_color is not None: self.change_text_color(new_text_color)
        if new_bg is not None: self.canvas.config(bg=new_bg)
        if self.canvas.winfo_children():
            for child in self.canvas.winfo_children():
                if "text" in child.keys():
                    child.config(fg=new_text_color)
        if buttons is not None:
            for button in buttons:
                if button is not None:
                    button.config(bg=new_fill)
        if labels is not None:
            for label in labels:
                if label is not None:
                    label.config(bg=new_fill, fg=new_text_color)

    def change_fill_color(self, new_color):
        self.fill = new_color
        self.create_images()
        self.create_labelframe()

    def change_text_color(self, new_color):
        self.fg = new_color
        self.canvas.itemconfig(self.text_item, fill=self.fg)

    def change_bg_color(self, new_bg):
        self.canvas.config(bg=new_bg)

    def get_label_width(self):
        bbox = self.canvas.bbox(self.text_item)
        width = bbox[2] - bbox[0]
        return width

    def set_label_text(self, new_text):
        if self.canvas is not None:
            self.canvas.itemconfig(self.text_item, text=new_text)

    def get_label_height(self):
        bbox = self.canvas.bbox(self.text_item)
        height = bbox[3] - bbox[1]
        return height

    def set_width(self, new_width):
        self.width = new_width
        self.create_labelframe()

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_radius(self):
        return self.radius

    def destroy(self):
        self.canvas.destroy()


bar_height = 0
pg_bar_width = 0
pg_bar_height = 0


class CustomProgressBar:

    def __init__(self, master, width, height,
                 bg=BLACK, pr_bar=BLACK, pr_bar_bg=WHITE, bar_bg=WHITE, bar_bg_accent=BGCOLOR,
                 radius=10, padding=4):
        self.new_progress_bar_fg = None
        global bar_height, pg_bar_width, pg_bar_height

        self.bg = bg
        self.bar_bg_accent = bar_bg_accent
        self.bar_bg = bar_bg
        self.pr_bar_bg = pr_bar_bg
        self.pr_bar = pr_bar
        self.width = width
        self.height = height
        self.fg = FONT_COLOR
        self.radius = radius
        self.padding = padding
        self.canvas = Canvas(master, width=width, height=height, bg=bg, highlightthickness=0)

        # Calculating progress bar foreground dimensions
        bar_height = self.height - self.padding * 2
        pg_bar_width = self.width - self.padding * 2
        pg_bar_height = self.height - self.padding * 2
        self.canvas.pack()

        self.progress_bar_fg = None
        self.progress_bar_bg = None

        self.create_pbar()

    def create_pbar(self):
        # Creating progress bar foreground
        self.progress_bar_bg = CustomLabelFrame(self.canvas,
                                                width=self.width,
                                                height=self.height,
                                                radius=self.radius,
                                                fill=self.bar_bg_accent,
                                                bg=self.bg)
        self.create_pbar_fg(width=self.radius + 1, height=pg_bar_height)

    def create_pbar_fg(self, width, height=30):
        # Creating progress bar background
        global bar_height
        self.progress_bar_fg = CustomLabelFrame(self.canvas,
                                                width=width,
                                                height=height,
                                                radius=self.radius // 2,
                                                fill=self.pr_bar,
                                                bg=self.bar_bg_accent)
        self.progress_bar_fg.canvas.place(x=self.padding, y=self.padding)

    def set_percentage(self, percentage):
        # Settings progress bar width based on percentage
        new_width = int(round(pg_bar_width * (percentage / 100)))
        if new_width > self.radius:
            self.create_pbar_fg(width=new_width, height=self.height - self.padding * 2)

    def config(self, bg):
        self.bg = bg
        self.canvas.config(bg=bg)
        self.progress_bar_bg.change_bg_color(bg)

    def change_pb_color(self, new_color):
        # Changing progress bar fill color
        self.progress_bar_fg.change_fill_color(new_color)

    def change_pb_bg_color(self, new_color):
        # Changing progress bar background fill color
        self.progress_bar_bg.change_fill_color(new_color)

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def place(self, x=0, y=0):
        self.canvas.place(x=x, y=y)
