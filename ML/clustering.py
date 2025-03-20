import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import pandas as pd
import seaborn as sns

# Génération de données synthétiques avec 5 variables
n_samples = 300
n_features = 5
n_clusters = 3

# Création des données avec 3 clusters distincts
X, y_true = make_blobs(
    n_samples=n_samples,
    n_features=n_features,
    centers=n_clusters,
    random_state=42
)

# Standardisation des données
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Application de la PCA
pca = PCA(n_components=2)  # On réduit à 2 dimensions pour la visualisation
X_pca = pca.fit_transform(X_scaled)

# Affichage de la variance expliquée
print("\nVariance expliquée par composante :")
for i, var in enumerate(pca.explained_variance_ratio_):
    print(f"Composante {i+1}: {var:.3f}")

# Application de K-means sur les données réduites
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
y_pred = kmeans.fit_predict(X_pca)

# Création d'un DataFrame pour visualisation
df = pd.DataFrame(X, columns=[f'Variable_{i+1}' for i in range(n_features)])
df['Cluster'] = y_pred

# Affichage des statistiques par cluster
print("\nStatistiques par cluster :")
print(df.groupby('Cluster').mean())

# Visualisation des clusters avec PCA
plt.figure(figsize=(10, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=y_pred, cmap='viridis')
plt.xlabel('Première composante principale')
plt.ylabel('Deuxième composante principale')
plt.title('Visualisation des Clusters après PCA')
plt.colorbar(label='Cluster')
plt.grid(True)
plt.show()

# Matrice de corrélation
plt.figure(figsize=(10, 8))
sns.heatmap(df.corr(), annot=True, cmap='coolwarm', center=0)
plt.title('Matrice de Corrélation')
plt.show()

# Évaluation de la qualité du clustering
from sklearn.metrics import silhouette_score
silhouette_avg = silhouette_score(X_pca, y_pred)
print(f"\nScore de silhouette moyen : {silhouette_avg:.3f}")

# Visualisation des centres des clusters
centers = kmeans.cluster_centers_
print("\nCentres des clusters (en espace PCA) :")
for i, center in enumerate(centers):
    print(f"\nCluster {i}:")
    print(f"PC1: {center[0]:.2f}")
    print(f"PC2: {center[1]:.2f}") 