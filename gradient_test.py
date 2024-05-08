import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk

root = tk.Tk()
root.geometry('500x500')
root.config(bg="grey")

# Create a label
label_text = "This is a label"
label = tk.Label(root, text=label_text, bg="grey", fg="black", font=("Helvetica", 12))
label.place(x=10, y=10)

# Get the dimensions of the label
label_width = label.winfo_reqwidth()
label_height = label.winfo_reqheight()

# Create a blank RGBA image with the same dimensions as the label
gradient_img = Image.new("RGBA", (label_width, label_height), (255, 255, 255, 0))

# Draw a horizontal gradient from solid white to fully transparent on the image
draw = ImageDraw.Draw(gradient_img)
for x in range(gradient_img.width):
    opacity = int(255 * (1 - x / gradient_img.width))  # Calculate opacity for each x-coordinate
    draw.line((x, 0, x, gradient_img.height), fill=(255, 255, 255, opacity))

# Create a PIL font object using the font attributes of the label widget

# Create another RGBA image for the label text and draw the label text onto it
label_img = Image.new("RGBA", (label_width, label_height), (255, 255, 255, 0))
draw_label = ImageDraw.Draw(label_img)
draw_label.text((0, 0), label_text, fill=(0, 0, 0, 255))

# Ensure both images have the same dimensions by resizing label_img if necessary
if gradient_img.size != label_img.size:
    label_img = label_img.resize(gradient_img.size)

# Composite the label text image over the gradient image
composite_img = Image.alpha_composite(gradient_img, label_img)

# Convert the composite image to a Tkinter-compatible format
composite_photo = ImageTk.PhotoImage(composite_img)

# Create a label to display the composite image
composite_label = tk.Label(root, image=composite_photo, bg="grey")
composite_label.place(x=10, y=10)

root.mainloop()
