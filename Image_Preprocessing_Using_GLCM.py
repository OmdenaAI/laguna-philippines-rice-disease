import os
import cv2
import numpy as np
from tkinter import Tk, Label, Button, filedialog


def browse_input_folder():
    input_folder = filedialog.askdirectory()
    input_folder_label.config(text=input_folder)

def browse_output_folder():
    output_folder = filedialog.askdirectory()
    output_folder_label.config(text=output_folder)

def browse_input_folder():
    input_folder = filedialog.askdirectory()
    input_folder_label.config(text=input_folder)

def browse_output_folder():
    output_folder = filedialog.askdirectory()
    output_folder_label.config(text=output_folder)

def segment_plant(image):
    mask = np.zeros(image.shape[:2], np.uint8)

    bgdModel = np.zeros((1, 65), np.float64)
    fgdModel = np.zeros((1, 65), np.float64)

    
    rect = (0, 0, image.shape[1] - 1, image.shape[0] - 1)

    cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 200, cv2.GC_INIT_WITH_RECT)

    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    

    segmented_image = image * mask2[:, :, np.newaxis]

    return segmented_image


def process_images():
    input_folder = input_folder_label.cget("text")
    output_folder = output_folder_label.cget("text")

    for filename in os.listdir(input_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img_path = os.path.join(input_folder, filename)
            img = cv2.imread(img_path)

            # Apply segmentation
            segmented_img = segment_plant(img)

            output_img_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_img_path, segmented_img)

    print("Processing complete.")

app = Tk()
app.title("Plant Image Preprocessing")

browse_input_button = Button(app, text="Browse Input Folder", command=browse_input_folder)
browse_input_button.grid(row=0, column=0)
input_folder_label = Label(app, text="")
input_folder_label.grid(row=0, column=1)

browse_output_button = Button(app, text="Browse Output Folder", command=browse_output_folder)
browse_output_button.grid(row=1, column=0)
output_folder_label = Label(app, text="")
output_folder_label.grid(row=1, column=1)

process_button = Button(app, text="Process Images", command=process_images)
process_button.grid(row=2, columnspan=2)

app.mainloop()
