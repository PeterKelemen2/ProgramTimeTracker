import dearpygui.dearpygui as dpg
from PIL import Image, ImageTk

# Create the Dear PyGui context
dpg.create_context()

# Create a Tkinter root window
root = dpg.create_viewport(title='Dear PyGui Example', width=800, height=600)

# Load the transparent image
transparent_image = Image.open("assets/accent_gradient.png")
transparent_photo = ImageTk.PhotoImage(transparent_image)

# Create a Dear PyGui window
with dpg.window(label="Hello, Dear PyGui!"):
    dpg.add_image(transparent_photo)

# Show the Dear PyGui viewport
dpg.show_viewport()

# Start Dear PyGui event loop
dpg.start_dearpygui()
