import os
import cv2
import numpy as np
from tkinter import Tk, Label, Button, Checkbutton, BooleanVar, Entry, filedialog
from PIL import Image, ImageOps, ImageFilter

def browse_input_folder():
    input_folder = filedialog.askdirectory()
    input_folder_label.config(text=input_folder)

def browse_output_folder():
    output_folder = filedialog.askdirectory()
    output_folder_label.config(text=output_folder)

def segment_plant(image):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_green = np.array([30, 30, 30])
    upper_green = np.array([90, 255, 255])
    mask = cv2.inRange(hsv_image, lower_green, upper_green)
    segmented_image = cv2.bitwise_and(image, image, mask=mask)
    return segmented_image

def process_images():
    input_folder = input_folder_label.cget("text")
    output_folder = output_folder_label.cget("text")

    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img_path = os.path.join(input_folder, filename)
            img = Image.open(img_path)

            if resize.get():
                width = int(width_entry.get())
                height = int(height_entry.get())
                img = img.resize((width, height))

            if grayscale.get():
                img = ImageOps.grayscale(img)

            if histogram_equalization.get():
                img = ImageOps.equalize(img)

            if gaussian_blur.get():
                radius = float(radius_entry.get())
                img = img.filter(ImageFilter.GaussianBlur(radius=radius))

            if segmentation.get():
                img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
                img = segment_plant(img)
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)

            output_img_path = os.path.join(output_folder, filename)
            img.save(output_img_path)

    print("Processing complete.")

app = Tk()
app.title("Plant Disease Image Preprocessing")


browse_input_button = Button(app, text="Browse Input Folder", command=browse_input_folder)
browse_input_button.grid(row=0, column=0)
input_folder_label = Label(app, text="")
input_folder_label.grid(row=0, column=1)

browse_output_button = Button(app, text="Browse Output Folder", command=browse_output_folder)
browse_output_button.grid(row=1, column=0)
output_folder_label = Label(app, text="")
output_folder_label.grid(row=1, column=1)


resize = BooleanVar()
resize_checkbutton = Checkbutton(app, text="Resize", variable=resize)
resize_checkbutton.grid(row=2, column=0)

grayscale = BooleanVar()
grayscale_checkbutton = Checkbutton(app, text="Grayscale", variable=grayscale)
grayscale_checkbutton.grid(row=3, column=0)

histogram_equalization = BooleanVar()
histogram_checkbutton = Checkbutton(app, text="Histogram Equalization", variable=histogram_equalization)
histogram_checkbutton.grid(row=4, column=0)

gaussian_blur = BooleanVar()
gaussian_checkbutton = Checkbutton(app, text="Gaussian Blur", variable=gaussian_blur)
gaussian_checkbutton.grid(row=5, column=0)

segmentation = BooleanVar()
segmentation_checkbutton = Checkbutton(app, text="Segmentation", variable=segmentation)
segmentation_checkbutton.grid(row=6, column=0)


width_label = Label(app, text="Width")
width_label.grid(row=2, column=1)
width_entry = Entry(app)
width_entry.grid(row=2, column=2)

height_label = Label(app, text="Height")
height_label.grid(row=3, column=1)
height_entry = Entry(app)
height_entry.grid(row=3, column=2)

radius_label = Label(app, text="Gaussian Blur Radius")
radius_label.grid(row=5, column=1)
radius_entry = Entry(app)
radius_entry.grid(row=5, column=2)


process_button = Button(app, text="Process Images", command=process_images)
process_button.grid(row=7, columnspan=3)

app.mainloop()