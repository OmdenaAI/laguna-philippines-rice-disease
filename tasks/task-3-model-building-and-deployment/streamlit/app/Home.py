import streamlit as st

st.set_page_config(
    page_title="Rice Disease Classification App",
    page_icon="👋",
)

st.title("Home Page")
st.image("app/artifactory/RiceDiseaseClassifier.jpeg", caption='', use_column_width=True)

st.header("The Problem")
st.write("""
Rice diseases are a major concern in the Philippines, a country that relies heavily on rice as a staple food. A variety of fungal, bacterial, and viral diseases can infect rice plants, causing reduced yield, lower quality, and even total crop loss. These diseases can be devastating to farmers, especially those with limited resources who cannot afford the cost of chemical treatments or disease-resistant seeds. Additionally, the high humidity and frequent rain in the Philippines create favorable conditions for the growth and spread of rice diseases.
""")

st.header("Want to know more?")
st.markdown("* [Omdena Page](https://omdena.com/chapter-challenges/creating-a-rice-disease-classifier-using-computer-vision-through-open-source-data/)")

st.sidebar.success("Select a page above.")
