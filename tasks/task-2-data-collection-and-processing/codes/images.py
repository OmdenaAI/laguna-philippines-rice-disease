import os
import cv2
import numpy as np
import imgaug.augmenters as iaa
from tkinter import Tk, Label, Button, Checkbutton, BooleanVar, Entry, filedialog
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
from skimage.feature import graycomatrix, graycoprops


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

def glcm(img, distances, angles, properties):
    gray_img = np.array(img, dtype=np.uint8)
    glcm_matrix = graycomatrix(gray_img, distances, angles)
    glcm_features = {}
    for prop in properties:
        glcm_features[prop] = graycoprops(glcm_matrix, prop)[0, 0]
    return glcm_features

def process_images():
    input_folder = input_folder_label.cget("text")
    output_folder = output_folder_label.cget("text")
    distances = [1]
    angles = [0]
    properties = ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM']

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

            if sharpness.get():
                sharpness_factor = float(sharpness_entry.get())
                img = ImageEnhance.Sharpness(img).enhance(sharpness_factor)

            if contrast.get():
                contrast_factor = float(contrast_entry.get())
                img = ImageEnhance.Contrast(img).enhance(contrast_factor)

            if augmentation.get():
                seq = iaa.Sequential([
                    iaa.Fliplr(0.5),
                    iaa.Flipud(0.5),
                    iaa.Affine(rotate=(-45, 45), mode="symmetric"),
                ])
                img = seq(image=np.array(img))

            if glcm_processing.get():
                img = ImageOps.grayscale(img)
                glcm_features = glcm(img, distances, angles, properties)
                output_img_path = os.path.join(output_folder, filename.split('.')[0] + '_glcm.csv')
                with open(output_img_path, 'w') as f:
                    f.write('Property,Value\n')
                    for prop, value in glcm_features.items():
                        f.write(f'{prop},{value}\n')
            else:
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

sharpness = BooleanVar()
sharpness_checkbutton = Checkbutton(app, text="Sharpness", variable=sharpness)
sharpness_checkbutton.grid(row=7, column=0)

contrast = BooleanVar()
contrast_checkbutton = Checkbutton(app, text="Contrast", variable=contrast)
contrast_checkbutton.grid(row=8, column=0)

augmentation = BooleanVar()
augmentation_checkbutton = Checkbutton(app, text="Augmentation", variable=augmentation)
augmentation_checkbutton.grid(row=9, column=0)

glcm_processing = BooleanVar()
glcm_checkbutton = Checkbutton(app, text="GLCM Preprocessing", variable=glcm_processing)
glcm_checkbutton.grid(row=10, column=0)

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

sharpness_label = Label(app, text="Sharpness")
sharpness_label.grid(row=7, column=1)
sharpness_entry = Entry(app)
sharpness_entry.grid(row=7, column=2)

contrast_label = Label(app, text="Contrast")
contrast_label.grid(row=8, column=1)
contrast_entry = Entry(app)
contrast_entry.grid(row=8, column=2)

process_button = Button(app, text="Process Images", command=process_images)
process_button.grid(row=11, columnspan=3)

app.mainloop()