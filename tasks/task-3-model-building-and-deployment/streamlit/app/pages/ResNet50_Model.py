import streamlit as st
import tensorflow as tf
import cv2
from PIL import Image, ImageOps
import numpy as np

# Suppress warnings
import warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

def load_model():
    model = tf.keras.models.load_model('app/artifactory/image_classification.hdf5')
    return model


with st.spinner('Model is being loaded..'):
    model = load_model()

st.write("""
         # Rice Disease Classifier
         """
         )

file = st.file_uploader("Upload the image to be classified", type=["jpg", "png"])
st.set_option('deprecation.showfileUploaderEncoding', False)


def upload_predict(upload_image, model):
    size = (180, 180)
    image = ImageOps.fit(upload_image, size, Image.ANTIALIAS)
    image = np.asarray(image)
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_resize = cv2.resize(img, dsize=(224, 224), interpolation=cv2.INTER_CUBIC)

    img_reshape = img_resize[np.newaxis, ...]

    prediction = model.predict(img_reshape)
    print(prediction)
    return prediction


if file is None:
    st.text("Please upload an image file")
else:
    image = Image.open(file)
    st.image(image, use_column_width=True)
    prediction = upload_predict(image, model)
    predicted_result = np.argmax(prediction)
    print(predicted_result)
    classfiers = ['bacterial_leaf_blight','bacterial_leaf_streak','bakanae','brown_spot','grassy_stunt_virus','healthy_rice_plant',
    'narrow_brown_spot','ragged_stunt_virus','rice_blast','rice_false_smut','sheath_blight','sheath_rot','stem_rot','tungro_virus']
    image_class = classfiers[predicted_result]
    confidence_score = prediction[0][predicted_result]
    st.write("The image is classified as", image_class)
    st.write("The similarity score is approximately", confidence_score, "/1")
    print("The image is classified as ", image_class, "with a similarity score of", confidence_score)
