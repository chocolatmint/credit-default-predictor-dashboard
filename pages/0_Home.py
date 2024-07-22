import streamlit as st
from streamlit_carousel import carousel
import base64

st.set_page_config(
    page_title="Welcome!",
    page_icon="🏠",
    layout="wide",
)

def get_base64_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()

st.markdown('<h4 style="text-align: center;">Welcome to</h4>', unsafe_allow_html=True)        
st.markdown('<h1 style="text-align: center;">Credit Card Default Predictor</h1>', unsafe_allow_html=True)
images = [
    dict(
        title="",
        text="",
        img="https://img.freepik.com/free-photo/person-paying-with-its-credit-card_23-2149167293.jpg?t=st=1721627125~exp=1721630725~hmac=a6dec684892c1c6e4996b538fbfc29405f24772fc7692581d31da43ab54e2c94&w=1480",
        link=""
    ),
    dict(
        title="",
        text="",
        img="https://img.freepik.com/free-photo/select-focus-credit-card-hand-young-handsome-man-mask-he-holding-paper-bag_1150-47122.jpg?t=st=1721627182~exp=1721630782~hmac=9b9b954516a63e44f2364f4e37253b1bdfc232b14cf9b15ac563e2ac730aa318&w=1480",
        link=""
    ),
]

carousel(items=images)
