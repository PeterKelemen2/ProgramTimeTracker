import tkinter as tk
from PIL import Image, ImageDraw, ImageTk

root = tk.Tk()
root.geometry('500x500')
root.config(bg="grey")

# Create a label
label = tk.Label(root, text="This is a label", bg="grey", fg="black")
label.place(x=10, y=15)

# Create a blank RGBA image with the same size as the label
gradient_img = Image.new("RGBA", (label.winfo_reqwidth(), label.winfo_reqheight()))

# Draw a horizontal gradient from solid white to fully transparent on the image
draw = ImageDraw.Draw(gradient_img)
for y in range(gradient_img.height * 2):
    opacity = int(255 * (1 - y / gradient_img.height))  # Calculate opacity for each y-coordinate
    draw.line((0, y, gradient_img.width, y), fill=(48, 55, 84, opacity))

# Convert the gradient image to a Tkinter-compatible format
gradient_photo = ImageTk.PhotoImage(gradient_img)

# Create a label to display the gradient image on top of the label
gradient_label = tk.Label(root, image=gradient_photo, bg="grey")
gradient_label.place(x=10, y=0)

root.mainloop()
