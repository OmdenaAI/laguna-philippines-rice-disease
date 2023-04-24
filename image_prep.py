import cv2
import numpy as np
import os

# Specify the input directory containing leaf images
input_dir = 'C:/Users/Rocelle Nathalie Ong/Downloads/initial/fungal_diseases/input/'

# Specify the output directory to save processed images
output_dir = 'C:/Users/Rocelle Nathalie Ong/Downloads/initial/fungal_diseases/processed_images/'

# Create the output directory if it does not exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through each image file in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        
        # Load the input image
        img = cv2.imread(os.path.join(input_dir, filename))

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to remove noise
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply Otsu's thresholding to segment the leaf from the background
        ret, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

        # Find contours in the binary image
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Find the largest contour (leaf) in the image
        areas = [cv2.contourArea(c) for c in contours]
        max_index = np.argmax(areas)
        max_contour = contours[max_index]

        # Create a mask of the same size as the input image
        mask = np.zeros(img.shape[:2], np.uint8)

        # Draw the contour on the mask
        cv2.drawContours(mask, [max_contour], 0, 255, -1)

        # Apply bitwise AND operation to remove the background
        masked_img = cv2.bitwise_and(img, img, mask=mask)

        # Save the processed image in the output directory
        output_filename = os.path.join(output_dir, filename)
        cv2.imwrite(output_filename, masked_img)
