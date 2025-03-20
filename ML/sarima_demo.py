import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_squared_error
import streamlit as st

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Démo SARIMA Simple",
    page_icon="📈",
    layout="wide"
)

# Titre et description
st.title("📈 Démonstration Simple de SARIMA")
st.markdown("""
Cette application montre comment utiliser le modèle SARIMA (Seasonal ARIMA) pour la prédiction de séries temporelles.
Nous allons générer des données synthétiques et faire des prédictions.
""")

def generate_synthetic_data(n_samples=1000):
    """Génère des données synthétiques avec une tendance et une saisonnalité"""
    t = np.linspace(0, 4*np.pi, n_samples)
    trend = 0.1 * t
    seasonal = np.sin(t) + 0.5 * np.sin(2*t)
    noise = np.random.normal(0, 0.1, n_samples)
    return trend + seasonal + noise

def train_sarima_model(data, order=(1,1,1), seasonal_order=(1,1,1,12)):
    """Entraîne un modèle SARIMA"""
    model = SARIMAX(data,
                    order=order,
                    seasonal_order=seasonal_order,
                    enforce_stationarity=False,
                    enforce_invertibility=False)
    results = model.fit(disp=False)
    return results

def plot_predictions(actual, predicted, title):
    """Affiche les prédictions et les valeurs réelles"""
    plt.figure(figsize=(12, 6))
    plt.plot(actual, label='Données réelles', color='blue')
    plt.plot(predicted, label='Prédictions', color='red', linestyle='--')
    plt.title(title)
    plt.legend()
    return plt.gcf()

def main():
    # Génération des données
    st.subheader("1. Génération des données synthétiques")
    n_samples = st.slider("Nombre d'échantillons", 100, 2000, 1000)
    data = generate_synthetic_data(n_samples)
    
    # Affichage des données
    fig = plt.figure(figsize=(12, 6))
    plt.plot(data)
    plt.title("Données synthétiques générées")
    st.pyplot(fig)
    
    # Paramètres du modèle SARIMA
    st.subheader("2. Configuration du modèle SARIMA")
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Ordre du modèle")
        p = st.slider("p (AR)", 0, 3, 1)
        d = st.slider("d (Différenciation)", 0, 2, 1)
        q = st.slider("q (MA)", 0, 3, 1)
    
    with col2:
        st.write("Ordre saisonnier")
        P = st.slider("P (AR saisonnier)", 0, 2, 1)
        D = st.slider("D (Différenciation saisonnière)", 0, 2, 1)
        Q = st.slider("Q (MA saisonnier)", 0, 2, 1)
        s = st.slider("Période saisonnière", 4, 24, 12)
    
    # Division train/test
    train_size = int(len(data) * 0.8)
    train_data = data[:train_size]
    test_data = data[train_size:]
    
    # Entraînement du modèle
    if st.button("Entraîner le modèle"):
        with st.spinner("Entraînement en cours..."):
            model = train_sarima_model(train_data, 
                                     order=(p,d,q),
                                     seasonal_order=(P,D,Q,s))
            
            # Prédictions
            forecast = model.forecast(steps=len(test_data))
            
            # Calcul de l'erreur
            mse = mean_squared_error(test_data, forecast)
            rmse = np.sqrt(mse)
            
            st.write(f"Erreur quadratique moyenne (RMSE): {rmse:.4f}")
            
            # Affichage des prédictions
            fig = plot_predictions(test_data, forecast, 
                                 "Comparaison des prédictions avec les données réelles")
            st.pyplot(fig)
            
            # Affichage des diagnostics du modèle
            st.subheader("Diagnostics du modèle")
            fig = model.plot_diagnostics(figsize=(12, 8))
            st.pyplot(fig)

if __name__ == "__main__":
    main() 