import streamlit as st
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz
from unidecode import unidecode
import matplotlib.pyplot as plt

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Simulation de Matching Client",
    page_icon="🔍",
    layout="wide"
)

# Fonction de génération de données
def generate_data(num_clients, error_rate=0.1):
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

def calculate_similarity_score(str1, str2):
    """Calcule le score de similarité entre deux chaînes."""
    # Si exactement identiques
    if str1 == str2:
        return 100
    
    # Sinon, utiliser le score de similarité brut
    return fuzz.ratio(normalize_string(str1), normalize_string(str2))

def match_clients(client_a, client_b, weights):
    # Calcul des scores individuels avec normalisation des chaînes
    nom_score = calculate_similarity_score(client_a['Nom'], client_b['Nom'])
    prenom_score = calculate_similarity_score(client_a['Prénom'], client_b['Prénom'])
    telephone_score = calculate_similarity_score(client_a['Téléphone'], client_b['Téléphone'])
    email_score = calculate_similarity_score(client_a['Email'], client_b['Email'])
    id_vehicule_score = calculate_similarity_score(client_a['ID_Véhicule'], client_b['ID_Véhicule'])
    immatriculation_score = calculate_similarity_score(client_a['Immatriculation'], client_b['Immatriculation'])
    
    # Calcul du score moyen
    score = (nom_score + prenom_score + email_score + telephone_score + id_vehicule_score + immatriculation_score) / 6
    
    return score, {
        'Nom': nom_score,
        'Prénom': prenom_score,
        'Email': email_score,
        'Téléphone': telephone_score,
        'ID_Véhicule': id_vehicule_score,
        'Immatriculation': immatriculation_score
    }

# Simulation de matching
def simulate_matching(clients, weights, threshold):
    matches = []
    
    # Créer un dictionnaire pour stocker les groupes de clients
    client_groups = {}
    next_group_id = 0
    
    # Comparer tous les clients entre eux
    for i, client_a in clients.iterrows():
        for j, client_b in clients.iterrows():
            if i < j:  # Éviter les comparaisons en double
                score, detail_scores = match_clients(client_a, client_b, weights)
                
                if score >= threshold:
                    matches.append({
                        'Client A': client_a['Nom'] + ' ' + client_a['Prénom'],
                        'Client B': client_b['Nom'] + ' ' + client_b['Prénom'],
                        'Score Global': score,
                        'Score Nom': detail_scores['Nom'],
                        'Score Prénom': detail_scores['Prénom'],
                        'Score Email': detail_scores['Email'],
                        'Score Téléphone': detail_scores['Téléphone'],
                        'Score ID Véhicule': detail_scores['ID_Véhicule'],
                        'Score Immatriculation': detail_scores['Immatriculation']
                    })
                    
                    # Regrouper les clients
                    if i in client_groups and j in client_groups:
                        # Les deux clients ont déjà des groupes, fusionner les groupes
                        group_a = client_groups[i]
                        group_b = client_groups[j]
                        if group_a != group_b:
                            for idx in client_groups:
                                if client_groups[idx] == group_b:
                                    client_groups[idx] = group_a
                    elif i in client_groups:
                        # Seulement le client A a un groupe, ajouter B au même groupe
                        client_groups[j] = client_groups[i]
                    elif j in client_groups:
                        # Seulement le client B a un groupe, ajouter A au même groupe
                        client_groups[i] = client_groups[j]
                    else:
                        # Aucun des clients n'a de groupe, créer un nouveau groupe
                        client_groups[i] = next_group_id
                        client_groups[j] = next_group_id
                        next_group_id += 1
    
    return pd.DataFrame(matches), client_groups

# Application Streamlit
def main():
    st.title("🔍 Simulation de Matching Client")
    st.markdown("""
    Cette application simule un système de matching client pour identifier et regrouper les événements appartenant au même client.
    Utilisez les contrôles ci-dessous pour configurer la simulation et analyser les résultats.
    """)
    
    # Sidebar pour les paramètres
    st.sidebar.title("Paramètres")
    
    # Explication des scores et seuils
    with st.sidebar.expander("ℹ️ Comprendre les scores et seuils"):
        st.markdown("""
        ### Calcul des scores
        - Chaque attribut (Nom, Prénom, Email, Téléphone) reçoit un score de similarité entre 0 et 100.
        - La méthode Jaro-Winkler est utilisée pour calculer la similarité entre deux chaînes.
        - Le score global est la moyenne des scores individuels.

        ### La confiance à confier aux différents seuils 
        - **Score global > 90%** : Correspondance quasi-certaine (très faible risque de faux positif)
        - **Score global 80-90%** : Bonne correspondance probable (faible risque de faux positif)
        - **Score global 70-80%** : Correspondance possible (risque modéré de faux positif)
        - **Score global < 70%** : Correspondance incertaine (risque élevé de faux positif)

        ### Scores par attribut
        - **> 90** : Attributs identiques ou très similaires
        - **70-90** : Attributs similaires avec quelques différences
        - **50-70** : Attributs partiellement similaires
        - **< 50** : Attributs différents
        """)
    
    # Configuration des données
    st.sidebar.subheader("Configuration des données")
    num_clients = st.sidebar.slider("Nombre de clients à générer", 10, 200, 50)
    error_rate = st.sidebar.slider("Taux d'erreur dans les données", 0.0, 0.5, 0.1, 
                                help="Pourcentage d'erreurs introduites dans les données pour simuler des données hétérogènes")
    
    # Seuil de similarité
    threshold = st.sidebar.slider("Seuil de similarité (%)", 0, 100, 80,
                               help="Score minimal pour considérer deux clients comme identiques")
    
    # Affichage du seuil avec code couleur
    threshold_color = "#ff0000" if threshold < 70 else "#ffa500" if threshold < 80 else "#008000"
    st.sidebar.markdown(f"""
    <div style='background-color: {threshold_color}; padding: 10px; border-radius: 5px; color: white;'>
    Seuil actuel: <strong>{threshold}%</strong><br>
    Risque de faux positifs: <strong>{'Élevé' if threshold < 70 else 'Modéré' if threshold < 80 else 'Faible'}</strong>
    </div>
    """, unsafe_allow_html=True)
    
    # Génération des données
    if st.button("Générer des données et lancer le matching"):
        with st.spinner("Génération des données en cours..."):
            clients = generate_data(num_clients, error_rate)
            
        st.subheader("Données clients générées")
        st.dataframe(clients)
        
        with st.spinner("Matching des clients en cours..."):
            matches_df, client_groups = simulate_matching(clients, {}, threshold)
        
        # Affichage des résultats
        st.subheader("Résultats du matching")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"Nombre total de matches trouvés : {len(matches_df)}")
            
            # Regrouper les clients en groupes
            groups = {}
            for idx, group_id in client_groups.items():
                if group_id not in groups:
                    groups[group_id] = []
                groups[group_id].append(idx)
            
            st.write(f"Nombre de groupes de clients identifiés : {len(groups)}")
        
        with col2:
            # Calculer les statistiques sur les scores
            if not matches_df.empty:
                st.write("Statistiques des scores :")
                score_mean = matches_df['Score Global'].mean()
                score_min = matches_df['Score Global'].min()
                score_max = matches_df['Score Global'].max()
                
                st.write(f"Score moyen : {score_mean:.2f}")
                st.write(f"Score minimum : {score_min:.2f}")
                st.write(f"Score maximum : {score_max:.2f}")
                
                # Indications sur la qualité des matches
                score_quality = "Excellente" if score_mean > 90 else "Bonne" if score_mean > 80 else "Moyenne" if score_mean > 70 else "Faible"
                st.markdown(f"**Qualité globale des matches: {score_quality}**")
        
        # Afficher les matches trouvés
        if not matches_df.empty:
            st.subheader("Exemples de comparaisons par niveau de qualité")
            
            # Créer un DataFrame avec les détails des clients
            comparison_data = []
            for _, match in matches_df.iterrows():
                client_a = clients[clients['Nom'] + ' ' + clients['Prénom'] == match['Client A']].iloc[0]
                client_b = clients[clients['Nom'] + ' ' + clients['Prénom'] == match['Client B']].iloc[0]
                
                # Calculer la qualité en fonction du score
                qualite = "✅ Excellente" if match['Score Global'] > 90 else "✅ Bonne" if match['Score Global'] > 80 else "⚠️ Moyenne" if match['Score Global'] > 70 else "❌ Faible"
                
                comparison_data.append({
                    'Score Global': match['Score Global'],
                    'Qualité': qualite,
                    'Client A - Nom': client_a['Nom'],
                    'Client A - Prénom': client_a['Prénom'],
                    'Client A - Email': client_a['Email'],
                    'Client A - Téléphone': client_a['Téléphone'],
                    'Client A - ID_Véhicule': client_a['ID_Véhicule'],
                    'Client A - Immatriculation': client_a['Immatriculation'],
                    'Client B - Nom': client_b['Nom'],
                    'Client B - Prénom': client_b['Prénom'],
                    'Client B - Email': client_b['Email'],
                    'Client B - Téléphone': client_b['Téléphone'],
                    'Client B - ID_Véhicule': client_b['ID_Véhicule'],
                    'Client B - Immatriculation': client_b['Immatriculation'],
                    'Score Nom': match['Score Nom'],
                    'Score Prénom': match['Score Prénom'],
                    'Score Email': match['Score Email'],
                    'Score Téléphone': match['Score Téléphone'],
                    'Score ID Véhicule': match['Score ID Véhicule'],
                    'Score Immatriculation': match['Score Immatriculation']
                })
            
            comparison_df = pd.DataFrame(comparison_data)
            
            # Grouper par qualité et sélectionner 3 exemples pour chaque niveau
            quality_groups = {
                "✅ Excellente": comparison_df[comparison_df['Score Global'] > 90],
                "✅ Bonne": comparison_df[(comparison_df['Score Global'] > 80) & (comparison_df['Score Global'] <= 90)],
                "⚠️ Moyenne": comparison_df[(comparison_df['Score Global'] > 70) & (comparison_df['Score Global'] <= 80)],
                "❌ Faible": comparison_df[comparison_df['Score Global'] <= 70]
            }
            
            for quality, group in quality_groups.items():
                if not group.empty:
                    st.markdown(f"### {quality}")
                    # Sélectionner 3 exemples aléatoires
                    examples = group.sample(n=min(3, len(group)))
                    
                    for _, row in examples.iterrows():
                        with st.expander(f"Score Global: {row['Score Global']:.1f}%"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("**Client A**")
                                st.write(f"Nom: {row['Client A - Nom']}")
                                st.write(f"Prénom: {row['Client A - Prénom']}")
                                st.write(f"Email: {row['Client A - Email']}")
                                st.write(f"Téléphone: {row['Client A - Téléphone']}")
                                st.write(f"ID Véhicule: {row['Client A - ID_Véhicule']}")
                                st.write(f"Immatriculation: {row['Client A - Immatriculation']}")
                            
                            with col2:
                                st.markdown("**Client B**")
                                st.write(f"Nom: {row['Client B - Nom']}")
                                st.write(f"Prénom: {row['Client B - Prénom']}")
                                st.write(f"Email: {row['Client B - Email']}")
                                st.write(f"Téléphone: {row['Client B - Téléphone']}")
                                st.write(f"ID Véhicule: {row['Client B - ID_Véhicule']}")
                                st.write(f"Immatriculation: {row['Client B - Immatriculation']}")
                            
                            st.markdown("**Scores par attribut**")
                            col3, col4, col5, col6, col7, col8 = st.columns(6)
                            
                            with col3:
                                st.metric("Score Nom", f"{row['Score Nom']:.1f}%")
                            with col4:
                                st.metric("Score Prénom", f"{row['Score Prénom']:.1f}%")
                            with col5:
                                st.metric("Score Email", f"{row['Score Email']:.1f}%")
                            with col6:
                                st.metric("Score Téléphone", f"{row['Score Téléphone']:.1f}%")
                            with col7:
                                st.metric("Score ID Véhicule", f"{row['Score ID Véhicule']:.1f}%")
                            with col8:
                                st.metric("Score Immatriculation", f"{row['Score Immatriculation']:.1f}%")
                            
                            # Afficher le score global
                            st.markdown(f"""
                            **Score Global: {row['Score Global']:.1f}%**
                            
                            *Note: Le score global est la moyenne des scores individuels de chaque attribut.*
                            """)
            
            # Distribution des scores
            st.subheader("Distribution des scores")
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.hist(matches_df['Score Global'], bins=20, color='#3498db', alpha=0.7)
            ax.axvline(x=90, color='green', linestyle='--', label='Excellent (>90)')
            ax.axvline(x=80, color='orange', linestyle='--', label='Bon (>80)')
            ax.axvline(x=70, color='red', linestyle='--', label='Moyen (>70)')
            ax.set_xlabel('Score global')
            ax.set_ylabel('Nombre de matches')
            ax.legend()
            st.pyplot(fig)
            
            # Visualisation des groupes de clients
            st.subheader("Groupes de clients identifiés")
            for group_id, indices in groups.items():
                with st.expander(f"Groupe {group_id} ({len(indices)} clients)"):
                    st.dataframe(clients.iloc[indices])
        else:
            st.info("Aucun match trouvé avec les paramètres actuels. Essayez de réduire le seuil de similarité ou d'ajuster les poids des attributs.")
        
        # Analyse des performances
        st.subheader("Analyse des performances des attributs")
        if not matches_df.empty:
            # Créer un graphique des scores par attribut
            fig, ax = plt.subplots(figsize=(10, 6))
            
            attributes = ['Score Nom', 'Score Prénom', 'Score Email', 'Score Téléphone', 'Score ID Véhicule', 'Score Immatriculation']
            means = [matches_df[attr].mean() for attr in attributes]
            
            # Définir les couleurs en fonction des scores
            colors = []
            for mean in means:
                if mean > 90:
                    colors.append('#2ecc71')  # vert - excellent
                elif mean > 80:
                    colors.append('#27ae60')  # vert foncé - bon
                elif mean > 70:
                    colors.append('#f39c12')  # orange - moyen
                elif mean > 50:
                    colors.append('#e67e22')  # orange foncé - faible
                else:
                    colors.append('#e74c3c')  # rouge - très faible
            
            ax.bar(attributes, means, color=colors)
            ax.set_ylim(0, 100)
            ax.set_ylabel('Score moyen')
            ax.set_title('Score moyen par attribut')
            
            # Ajouter des lignes de référence
            ax.axhline(y=90, color='green', linestyle='--', alpha=0.5)
            ax.axhline(y=70, color='red', linestyle='--', alpha=0.5)
            
            # Ajouter les valeurs sur les barres
            for i, v in enumerate(means):
                ax.text(i, v + 2, f"{v:.1f}", ha='center')
            
            st.pyplot(fig)
            
            # Recommandations
            st.subheader("Recommandations")
            
            recommendations = []
            
            # Analyser l'efficacité des attributs
            low_score_attributes = [(attr.replace('Score ', ''), score) for attr, score in zip(attributes, means) if score < 70]
            if low_score_attributes:
                for attr, score in low_score_attributes:
                    recommendations.append(f"L'attribut '{attr}' a un score moyen bas ({score:.1f}). Considérez améliorer la qualité des données pour cet attribut.")
            
            # Analyser le seuil
            if matches_df['Score Global'].min() < threshold * 0.9:
                recommendations.append(f"Certains matches ont un score proche du seuil ({threshold}). Considérez ajuster légèrement le seuil pour éviter les faux négatifs.")
            
            if not recommendations:
                recommendations.append("Le modèle de matching semble bien fonctionner avec les paramètres actuels.")
            
            for rec in recommendations:
                st.write(f"• {rec}")
            
            # Tableau des seuils recommandés
            st.subheader("Guide des seuils recommandés")
            seuil_df = pd.DataFrame({
                "Seuil": ["90% et plus", "80% - 90%", "70% - 80%", "Moins de 70%"],
                "Interprétation": [
                    "Correspondance quasi-certaine", 
                    "Bonne correspondance probable", 
                    "Correspondance possible", 
                    "Correspondance incertaine"
                ],
                "Risque de faux positifs": ["Très faible", "Faible", "Modéré", "Élevé"],
                "Recommandation": [
                    "Associer automatiquement les clients", 
                    "Associer les clients avec vérification périodique", 
                    "Vérification manuelle recommandée", 
                    "Ne pas associer automatiquement"
                ]
            })
            st.table(seuil_df)

if __name__ == "__main__":
    main() 