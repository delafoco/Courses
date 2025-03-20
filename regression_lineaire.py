import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

# Génération de données synthétiques
np.random.seed(42)
X = 2 * np.random.rand(100, 1)
y = 4 + 3 * X + np.random.randn(100, 1)

# Division en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Création et entraînement du modèle
model = LinearRegression()
model.fit(X_train, y_train)

# Prédictions
y_pred = model.predict(X_test)

# Évaluation du modèle
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Pente (coefficient): {model.coef_[0][0]:.2f}")
print(f"Ordonnée à l'origine: {model.intercept_[0]:.2f}")
print(f"Erreur quadratique moyenne: {mse:.2f}")
print(f"Score R²: {r2:.2f}")

# Visualisation
plt.figure(figsize=(10, 6))
plt.scatter(X_test, y_test, color='blue', label='Données réelles')
plt.plot(X_test, y_pred, color='red', label='Régression linéaire')
plt.xlabel('X')
plt.ylabel('y')
plt.title('Régression Linéaire')
plt.legend()
plt.grid(True)
plt.show() 