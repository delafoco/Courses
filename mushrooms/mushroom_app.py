import streamlit as st
from PIL import Image
from mushroom_model.mushroom_model import MushroomModel

# Configuration de la page
st.set_page_config(
    page_title="Classificateur de Champignons",
    page_icon="🍄",
    layout="wide"
)

# ... [rest of the code remains unchanged] ... 