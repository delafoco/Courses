import pandas as pd
import numpy as np
from unidecode import unidecode

def generate_data(num_clients, error_rate=0.1):
    """Génère des données clients avec des variations et erreurs"""
    data = []
    
    # Liste plus large de noms et prénoms pour plus de variations
    noms = ["Martin", "Dubois", "Thomas", "Richard", "Petit", "Durand", "Leroy", "Moreau", "Simon", "Laurent",
            "Bernard", "Robert", "Michel", "Garcia", "David", "Bertrand", "Roux", "Vincent", "Fournier", "Morel"]
    prenoms = ["Jean", "Marie", "Pierre", "Michel", "Sophie", "Catherine", "Nicolas", "Isabelle", "Philippe", "Anne",
               "Claude", "Lucas", "Emma", "Léa", "Hugo", "Louis", "Jules", "Alice", "Lina", "Noah"]
    
    for i in range(num_clients):
        nom = noms[i % len(noms)]
        prenom = prenoms[i % len(prenoms)]
        id_vehicule = f"VEH{i:05d}"
        immatriculation = f"AB-{i%999:03d}-CD"
        email = f"{prenom.lower()}.{nom.lower()}@example.com"
        telephone = f"01{i%99:02d}345678"
        
        # Introduire des erreurs aléatoires pour simuler des données hétérogènes
        if np.random.rand() < error_rate:
            # Erreurs plus variées dans le nom
            error_type = np.random.choice(['suppression', 'ajout', 'substitution', 'inversion'])
            if error_type == 'suppression':
                nom = nom[:-1] if len(nom) > 3 else nom
            elif error_type == 'ajout':
                nom = nom + ('e' if nom[-1] != 'e' else 'a')
            elif error_type == 'substitution':
                pos = np.random.randint(0, len(nom))
                nom = nom[:pos] + ('e' if nom[pos] != 'e' else 'a') + nom[pos+1:]
            else:  # inversion
                if len(nom) > 3:
                    pos = np.random.randint(0, len(nom)-1)
                    nom = nom[:pos] + nom[pos+1] + nom[pos] + nom[pos+2:]
        
        if np.random.rand() < error_rate:
            # Erreurs plus variées dans le prénom
            error_type = np.random.choice(['suppression', 'ajout', 'substitution', 'inversion'])
            if error_type == 'suppression':
                prenom = prenom[:-1] if len(prenom) > 3 else prenom
            elif error_type == 'ajout':
                prenom = prenom + ('s' if prenom[-1] != 's' else 'e')
            elif error_type == 'substitution':
                pos = np.random.randint(0, len(prenom))
                prenom = prenom[:pos] + ('e' if prenom[pos] != 'e' else 'a') + prenom[pos+1:]
            else:  # inversion
                if len(prenom) > 3:
                    pos = np.random.randint(0, len(prenom)-1)
                    prenom = prenom[:pos] + prenom[pos+1] + prenom[pos] + prenom[pos+2:]
        
        if np.random.rand() < error_rate:
            # Erreurs plus variées dans l'email
            error_type = np.random.choice(['domaine', 'format', 'caractères'])
            if error_type == 'domaine':
                email = email.replace('@example.com', '@gmail.com')
            elif error_type == 'format':
                email = email.replace('.', '_')
            else:  # caractères
                email = email.replace('a', '4').replace('e', '3').replace('i', '1').replace('o', '0')
        
        if np.random.rand() < error_rate:
            # Erreurs plus variées dans le téléphone
            error_type = np.random.choice(['format', 'chiffres', 'longueur'])
            if error_type == 'format':
                telephone = telephone.replace('-', ' ').replace(' ', '')
            elif error_type == 'chiffres':
                pos = np.random.randint(0, len(telephone))
                telephone = telephone[:pos] + str(np.random.randint(0, 10)) + telephone[pos+1:]
            else:  # longueur
                if np.random.rand() < 0.5:
                    telephone = telephone[:-1]  # trop court
                else:
                    telephone = telephone + str(np.random.randint(0, 10))  # trop long
        
        # Ajouter des erreurs dans l'ID véhicule
        if np.random.rand() < error_rate:
            error_type = np.random.choice(['chiffres', 'format', 'longueur'])
            if error_type == 'chiffres':
                pos = np.random.randint(3, len(id_vehicule))
                id_vehicule = id_vehicule[:pos] + str(np.random.randint(0, 10)) + id_vehicule[pos+1:]
            elif error_type == 'format':
                id_vehicule = id_vehicule.replace('VEH', 'VH')
            else:  # longueur
                if np.random.rand() < 0.5:
                    id_vehicule = id_vehicule[:-1]  # trop court
                else:
                    id_vehicule = id_vehicule + str(np.random.randint(0, 10))  # trop long
        
        # Ajouter des erreurs dans l'immatriculation
        if np.random.rand() < error_rate:
            error_type = np.random.choice(['chiffres', 'format', 'lettres'])
            if error_type == 'chiffres':
                pos = np.random.randint(3, 6)
                immatriculation = immatriculation[:pos] + str(np.random.randint(0, 10)) + immatriculation[pos+1:]
            elif error_type == 'format':
                immatriculation = immatriculation.replace('-', ' ')
            else:  # lettres
                pos = np.random.randint(0, 2)
                immatriculation = immatriculation[:pos] + chr(np.random.randint(65, 91)) + immatriculation[pos+1:]
        
        data.append({
            'Nom': nom,
            'Prénom': prenom,
            'ID_Véhicule': id_vehicule,
            'Immatriculation': immatriculation,
            'Email': email,
            'Téléphone': telephone,
            'Date': pd.Timestamp.now() - pd.Timedelta(days=np.random.randint(1, 100))
        })
        
        # Ajouter des doublons avec des variations plus importantes
        if i % 5 == 0:
            nom_alt = nom
            prenom_alt = prenom
            email_alt = email
            telephone_alt = telephone
            id_vehicule_alt = id_vehicule
            immatriculation_alt = immatriculation
            
            # Variations plus importantes pour les doublons
            if np.random.rand() < 0.3:
                nom_alt = nom.upper()
            if np.random.rand() < 0.3:
                prenom_alt = prenom.upper()
            if np.random.rand() < 0.3:
                # Variations d'email plus importantes
                email_variations = [
                    email.replace('@example.com', '@gmail.com'),
                    email.replace('.', '_'),
                    email.replace('a', '4').replace('e', '3').replace('i', '1').replace('o', '0'),
                    f"{prenom.lower()}{nom.lower()}@example.com",
                    f"{nom.lower()}.{prenom.lower()}@example.com"
                ]
                email_alt = np.random.choice(email_variations)
            if np.random.rand() < 0.3:
                # Variations de téléphone plus importantes
                telephone_variations = [
                    telephone.replace('-', ' ').replace(' ', ''),
                    telephone.replace('01', '06'),
                    telephone.replace('01', '07'),
                    telephone[:-1] + str(np.random.randint(0, 10)),
                    telephone + str(np.random.randint(0, 10))
                ]
                telephone_alt = np.random.choice(telephone_variations)
            if np.random.rand() < 0.3:
                # Variations d'ID véhicule plus importantes
                id_vehicule_variations = [
                    id_vehicule.replace('VEH', 'VH'),
                    id_vehicule.replace('VEH', 'VEH-'),
                    id_vehicule[:-1] + str(np.random.randint(0, 10)),
                    id_vehicule + str(np.random.randint(0, 10))
                ]
                id_vehicule_alt = np.random.choice(id_vehicule_variations)
            if np.random.rand() < 0.3:
                # Variations d'immatriculation plus importantes
                immatriculation_variations = [
                    immatriculation.replace('-', ' '),
                    immatriculation.replace('AB', 'BA'),
                    immatriculation.replace('CD', 'DC'),
                    immatriculation.replace('-', '')
                ]
                immatriculation_alt = np.random.choice(immatriculation_variations)
                
            data.append({
                'Nom': nom_alt,
                'Prénom': prenom_alt,
                'ID_Véhicule': id_vehicule_alt,
                'Immatriculation': immatriculation_alt,
                'Email': email_alt,
                'Téléphone': telephone_alt,
                'Date': pd.Timestamp.now() - pd.Timedelta(days=np.random.randint(1, 100))
            })
            
    return pd.DataFrame(data)

def normalize_string(s):
    """Convertit une chaîne en minuscules et supprime les accents."""
    return unidecode(str(s).lower()) 