#!pip install keras tensorflow scikit-learn pillow seaborn
# Trained on 80 epochs at Batch size 256 with Learning Rate of 0.001 under 50 seconds!!

from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np

import streamlit as st
import tensorflow as tf

# Suppress warnings
import warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)
# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

def load_model_teachable():
    # Load the model
    model = tf.keras.models.load_model("app/artifactory/keras_model.h5")
    return model

with st.spinner('Model is being loaded..'):
    model = load_model_teachable()

st.write("""
         # Teachable Machine Model
         """
         )

file = st.file_uploader("Upload the image to be classified", type=["jpg", "png"])
st.set_option('deprecation.showfileUploaderEncoding', False)


def upload_predict_teachable(image, model, class_names):

    # Create the array of the right shape to feed into the keras model
    # The 'length' or number of images you can put into the array is
    # determined by the first position in the shape tuple, in this case 1
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image_RGB = image.convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    # size = (224, 224)
    # image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    image_resized = image_RGB.resize((224, 224), resample=Image.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image_resized)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    return prediction


if file is None:
    st.text("Please upload an image file")
else:
    image = Image.open(file)
    st.image(image, use_column_width=True)
    # Load the labels
    class_names = open("app/artifactory/labels.txt", "r").readlines()
    prediction = upload_predict_teachable(image, model,class_names)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    st.write("The image is classified as", class_name)
    st.write("The similarity score is approximately", confidence_score, "/1")
    print("The image is classified as ", class_name, "with a similarity score of", confidence_score)