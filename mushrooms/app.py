import streamlit as st
import tensorflow as tf
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np
from PIL import Image
import io
import os

# Configuration de la page
st.set_page_config(
    page_title="Classificateur de Champignons",
    page_icon="🍄",
    layout="wide"
)

# Titre et description
st.title("🍄 Classificateur de Champignons")
st.markdown("""
Cette application utilise un modèle de deep learning (ResNet50) pour identifier les champignons dans vos images.
""")

# Fonction pour sauvegarder le modèle
def save_model(model, path='mushroom_model'):
    if not os.path.exists(path):
        os.makedirs(path)
    model.save(f'{path}/model.h5')
    st.success(f"Modèle sauvegardé dans {path}/model.h5")

# Chargement du modèle
@st.cache_resource
def load_model(model_path=None):
    if model_path and os.path.exists(model_path):
        model = tf.keras.models.load_model(model_path)
        st.info("Modèle personnalisé chargé")
    else:
        model = ResNet50(weights='imagenet')
        st.info("Modèle ResNet50 pré-entraîné chargé")
    return model

# Fonction de prétraitement de l'image
def preprocess_image(img):
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    return img_array

# Fonction de prédiction
def predict_mushroom(model, img_array):
    predictions = model.predict(img_array)
    results = decode_predictions(predictions, top=5)[0]
    return results

# Interface utilisateur
def main():
    # Sélection du modèle
    st.sidebar.title("Configuration du modèle")
    model_choice = st.sidebar.radio(
        "Choisir le modèle",
        ["ResNet50 pré-entraîné", "Modèle personnalisé"]
    )

    if model_choice == "Modèle personnalisé":
        uploaded_model = st.sidebar.file_uploader("Charger votre modèle (.h5)", type=['h5'])
        if uploaded_model:
            # Sauvegarder temporairement le modèle uploadé
            with open("temp_model.h5", "wb") as f:
                f.write(uploaded_model.getvalue())
            model = load_model("temp_model.h5")
        else:
            model = load_model()
    else:
        model = load_model()

    # Bouton pour sauvegarder le modèle
    if st.sidebar.button("Sauvegarder le modèle"):
        save_model(model)
    
    # Zone de téléchargement d'image
    uploaded_file = st.file_uploader("Choisissez une image de champignon", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file is not None:
        # Affichage de l'image
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Image téléchargée")
            image = Image.open(uploaded_file)
            st.image(image, use_column_width=True)
        
        # Bouton de prédiction
        if st.button("Analyser l'image"):
            with st.spinner("Analyse en cours..."):
                # Prétraitement et prédiction
                img_array = preprocess_image(image)
                results = predict_mushroom(model, img_array)
                
                # Affichage des résultats
                with col2:
                    st.subheader("Résultats de l'analyse")
                    for i, (id, label, prob) in enumerate(results):
                        st.write(f"{i+1}. {label}: {prob*100:.2f}%")
                        
                # Avertissement
                st.warning("""
                ⚠️ **Attention**: Cette application est à des fins de démonstration uniquement. 
                Ne vous fiez pas uniquement à cette analyse pour identifier des champignons comestibles.
                Consultez toujours un expert en mycologie pour une identification sûre.
                """)

if __name__ == "__main__":
    main() 