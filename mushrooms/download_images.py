import os
import requests
import time
from PIL import Image
from io import BytesIO
import random
from urllib.parse import quote

# Dictionnaire des espèces de champignons et leurs noms scientifiques
MUSHROOMS = {
    'amanite_tue_mouches': ['Amanita muscaria', 'fly agaric', 'amanite tue mouches'],
    'cep': ['Boletus edulis', 'porcini mushroom', 'cèpe'],
    'girolle': ['Cantharellus cibarius', 'chanterelle', 'girolle'],
    'chanterelle': ['Cantharellus cibarius', 'chanterelle', 'girolle'],
    'bolet': ['Boletus', 'boletus mushroom', 'bolet'],
    'amanite_rouge': ['Amanita rubescens', 'blusher', 'amanite rouge'],
    'amanite_phalloide': ['Amanita phalloides', 'death cap', 'amanite phalloïde'],
    'coprin': ['Coprinus comatus', 'shaggy ink cap', 'coprin chevelu'],
    'pied_bleu': ['Lepista nuda', 'wood blewit', 'pied bleu'],
    'meunier': ['Clitopilus prunulus', 'miller mushroom', 'meunier']
}

def download_image(url, save_path):
    """Télécharge une image depuis une URL et la sauvegarde"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            img = Image.open(BytesIO(response.content))
            # Vérifier si l'image est valide
            img.verify()
            img = Image.open(BytesIO(response.content))
            # Redimensionner si nécessaire
            if img.size[0] < 224 or img.size[1] < 224:
                return False
            img.save(save_path, 'JPEG', quality=85)
            return True
    except Exception as e:
        print(f"Erreur lors du téléchargement de {url}: {str(e)}")
    return False

def search_and_download_images(species, num_images=50):
    """Recherche et télécharge des images pour une espèce de champignon"""
    # Créer le dossier s'il n'existe pas
    save_dir = os.path.join(os.path.dirname(__file__), 'data', 'train', species)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # Rechercher des images pour chaque terme de recherche
    for search_term in MUSHROOMS[species]:
        print(f"Recherche d'images pour {search_term}...")
        
        # Construire l'URL de recherche
        search_url = f"https://www.bing.com/images/search?q={quote(search_term)}&qft=+filterui:photo-photo&FORM=IRFLTR"
        
        # Faire la requête
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(search_url, headers=headers)
        
        # Extraire les URLs des images
        if response.status_code == 200:
            content = response.text
            # Rechercher les URLs des images dans le contenu
            image_urls = []
            for line in content.split('\n'):
                if 'murl&quot;:&quot;' in line:
                    url = line.split('murl&quot;:&quot;')[1].split('&quot;')[0]
                    if url.startswith('http'):
                        image_urls.append(url)
            
            # Télécharger les images
            for i, url in enumerate(image_urls[:num_images]):
                filename = f"{species}_{i+1}.jpg"
                save_path = os.path.join(save_dir, filename)
                
                if download_image(url, save_path):
                    print(f"Image téléchargée: {filename}")
                
                # Pause pour éviter de surcharger
                time.sleep(random.uniform(1, 3))

def main():
    # Créer le dossier data s'il n'existe pas
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Créer le dossier train s'il n'existe pas
    train_dir = os.path.join(data_dir, 'train')
    if not os.path.exists(train_dir):
        os.makedirs(train_dir)
    
    # Télécharger des images pour chaque espèce
    for species in MUSHROOMS.keys():
        print(f"\nTéléchargement des images pour {species}...")
        search_and_download_images(species)
        # Pause entre les espèces
        time.sleep(random.uniform(2, 4))

if __name__ == "__main__":
    main() 