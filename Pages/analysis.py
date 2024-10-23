import streamlit as st
import pandas as pd

def load_raw_commune_data(commune_path):
    """
    Charge le fichier CSV brut des données communales et le retourne sous forme de DataFrame.
    """
    df_communes = pd.read_csv(commune_path)  # Charger les données du fichier CSV des communes
    return df_communes

def load_and_clean_data(presidentielle_path, commune_path):
    """
    Charge et nettoie les données des fichiers CSV/XLS des élections présidentielles et des communes.
    Retourne les DataFrames nettoyés et fusionnés.
    """

    # Charger le fichier Excel des résultats de la présidentielle sans ignorer les lignes
    df_presidentielle_brut = pd.read_excel(presidentielle_path, engine='xlrd')  # Sans 'skiprows'
    
    # Charger les données avec 'skiprows' pour ignorer les 3 premières lignes
    df_presidentielle = pd.read_excel(presidentielle_path, engine='xlrd', skiprows=3)

    # Charger les données brutes des communes
    df_communes = load_raw_commune_data(commune_path)

    # Sélectionner les colonnes pertinentes dans le dataset présidentiel
    columns_to_keep = [
        'Code du département', 'Libellé du département', 'Code de la commune', 'Libellé de la commune',
        'Inscrits', 'Abstentions', 'Votants', 'Blancs', 'Nuls', 'Exprimés'
    ]

    # Ajouter les colonnes pour les noms, prénoms et voix des candidats
    for i in range(11):  # Boucle pour gérer les colonnes de plusieurs candidats
        if i == 0:
            columns_to_keep.extend([f'Nom', f'Prénom', f'Voix'])
        else:
            columns_to_keep.extend([f'Nom.{i}', f'Prénom.{i}', f'Voix.{i}'])

    # Nettoyer le dataset présidentiel en sélectionnant uniquement les colonnes pertinentes
    df_presidentielle_clean = df_presidentielle[columns_to_keep].copy()

    # Convertir les codes de département et commune en chaînes de caractères et créer un code combiné unique
    df_presidentielle_clean['Code du département'] = df_presidentielle_clean['Code du département'].astype(str)
    df_presidentielle_clean['Code de la commune'] = df_presidentielle_clean['Code de la commune'].astype(str)
    df_presidentielle_clean['code_commune_combined'] = df_presidentielle_clean['Code du département'] + df_presidentielle_clean['Code de la commune'].str.zfill(3)

    # Nettoyer les données des communes en sélectionnant les colonnes pertinentes
    columns_to_keep_communes = [
        'code_commune_INSEE', 'nom_commune_postal', 'code_postal', 
        'latitude', 'longitude', 'code_commune', 'nom_commune_complet', 
        'code_departement', 'nom_departement', 'code_region', 'nom_region'
    ]
    df_communes_clean = df_communes[columns_to_keep_communes].copy()
    df_communes_clean['code_commune_INSEE'] = df_communes_clean['code_commune_INSEE'].astype(str)

    # Fusionner les deux datasets (présidentiel et communes) sur les codes INSEE et combiné
    df_combined = pd.merge(
        df_presidentielle_clean, 
        df_communes_clean, 
        left_on='code_commune_combined', 
        right_on='code_commune_INSEE', 
        how='left'  # Jointure gauche pour conserver toutes les données présidentielles
    )

    # Stocker les datasets nettoyés et fusionnés dans l'état de la session Streamlit
    st.session_state['df_presidentielle_clean'] = df_presidentielle_clean
    st.session_state['df_communes_clean'] = df_communes_clean
    st.session_state['df'] = df_combined
    
    return df_presidentielle_brut, df_presidentielle_clean, df_communes_clean, df_combined

def show_analysis():
    """
    Affiche la page d'analyse sur Streamlit, incluant les datasets bruts, nettoyés et fusionnés.
    """
    st.title("Page d'Analyse 📊")

    # Chemins vers les fichiers de données
    presidentielle_path = "./Presidentielle_2017_Resultats_Communes_Tour_1_c.xls"
    commune_path = "./communes-departement-region.csv"

    # Afficher les datasets bruts avant le nettoyage
    st.header("Données Brutes et Après Nettoyage")
    
    # Charger les datasets bruts et nettoyés
    df_presidentielle_brut, df_presidentielle_clean, df_communes_clean, df_combined = load_and_clean_data(presidentielle_path, commune_path)

    # Afficher les premières lignes du dataset présidentiel brut (sans skiprows)
    st.subheader("Données Brutes des Élections Présidentielles (Sans Ignorer les 3 premières lignes)")
    st.write(df_presidentielle_brut.head(10))

    # Afficher les premières lignes du dataset présidentiel après 'skiprows'
    st.subheader("Données des Élections Présidentielles (Après Ignorance des 3 premières lignes)")
    st.write(df_presidentielle_clean.head(10))

    # Afficher les premières lignes du dataset des communes brut
    st.subheader("Données Brutes des Communes (10 premières lignes)")
    st.write(df_communes_clean.head(10))

    # Afficher les premières lignes du dataset fusionné
    st.subheader("Données Fusionnées (10 premières lignes)")
    st.write(df_combined.head(10))

    # Vérification de l'agrégation des votes par département
    st.header("Vérification de l'Agrégation des Votes par Département")
    verify_aggregation(df_combined)

def verify_aggregation(df_combined):
    """
    Agrège les votes par département et affiche les 10 départements avec le plus de voix.
    """
    # Agréger les votes par département
    df_agg = df_combined.groupby('Code du département')['Voix'].sum().reset_index()

    # Trier les départements par le nombre de voix et afficher les 10 premiers
    df_top_departments = df_agg.sort_values(by='Voix', ascending=False).head(10)
    st.write("Top 10 des départements avec le plus de voix après agrégation :")
    st.write(df_top_departments)
