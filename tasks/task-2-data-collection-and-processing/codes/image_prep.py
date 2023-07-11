import cv2
import numpy as np
import os
from tkinter import filedialog
from tkinter import *


def preprocess_images(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            img = cv2.imread(os.path.join(input_dir, filename))
            img = cv2.resize(img, (224, 224))
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (5, 5), 0)
            ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            areas = [cv2.contourArea(c) for c in contours]
            max_index = np.argmax(areas)
            max_contour = contours[max_index]
            mask = np.zeros(img.shape[:2], np.uint8)
            cv2.drawContours(mask, [max_contour], 0, 255, -1)
            masked_img = cv2.bitwise_and(img, img, mask=mask)
            output_filename = os.path.join(output_dir, filename)
            cv2.imwrite(output_filename, masked_img)


def browse_input_folder():
    global input_folder_path
    input_folder_path = filedialog.askdirectory()
    input_folder_label.config(text=input_folder_path)


def browse_output_folder():
    global output_folder_path
    output_folder_path = filedialog.askdirectory()
    output_folder_label.config(text=output_folder_path)


def start_preprocessing():
    if input_folder_path and output_folder_path:
        preprocess_images(input_folder_path, output_folder_path)
        status_label.config(text="Image preprocessing completed!")
    else:
        status_label.config(text="Please select both input and output folders.")


# Create the main Tkinter window
root = Tk()
root.title("Image Preprocessing")
root.geometry("500x200")
root.resizable(False, False)

input_folder_path = ""
output_folder_path = ""

# Create and position the input folder button and label
input_folder_button = Button(root, text="Browse Input Folder", command=browse_input_folder)
input_folder_button.grid(row=0, column=0, padx=10, pady=10)
input_folder_label = Label(root, text="")
input_folder_label.grid(row=0, column=1, padx=10, pady=10)

# Create and position the output folder button and label
output_folder_button = Button(root, text="Browse Output Folder", command=browse_output_folder)
output_folder_button.grid(row=1, column=0, padx=10, pady=10)
output_folder_label = Label(root, text="")
output_folder_label.grid(row=1, column=1, padx=10, pady=10)

# Create and position the start button and status label
start_button = Button(root, text="Start Preprocessing", command=start_preprocessing)
start_button.grid(row=2, column=0, padx=10, pady=10)
status_label = Label(root, text="")
status_label.grid(row=2, column=1, padx=10, pady=10)

# Start the Tkinter main loop
root.mainloop()
