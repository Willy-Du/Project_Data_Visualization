import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from Pages.analysis import load_and_clean_data


def load_data_if_needed():
    # Cette fonction vérifie si les données sont déjà chargées dans la session
    # Si ce n'est pas le cas, elle appelle la fonction `load_and_clean_data` pour charger les données
    if 'df' not in st.session_state:
        presidentielle_path = "./Presidentielle_2017_Resultats_Communes_Tour_1_c.xls"
        commune_path = "./communes-departement-region.csv"
        load_and_clean_data(presidentielle_path, commune_path)


def show_visualizations():
    st.title("Visualizations Page 📈")

    # Vérifie si les données sont chargées dans la session
    if 'df' in st.session_state:
        df = st.session_state['df']

        st.write("Available columns in the DataFrame:")
        st.write(df.columns)

        # 1. Bar chart: Total Votes by Candidate (Selected Candidates)
        st.title("Bar Chart - Total Votes for Selected Candidates")
        # Liste des candidats que nous voulons visualiser
        selected_candidates = ['LE PEN', 'MÉLENCHON', 'MACRON', 'FILLON']
        # Filtrage du DataFrame pour ne garder que les lignes correspondantes à ces candidats
        filtered_df = df[df['Nom'].isin(selected_candidates)]
        # Calcul du total des voix pour chaque candidat sélectionné
        voix_totales_filtered = [filtered_df[filtered_df['Nom'] == candidat]['Voix'].sum() for candidat in selected_candidates]

        # Création du graphique à barres
        fig1, ax1 = plt.subplots()
        # Création des barres pour chaque candidat avec une palette de couleurs unique
        ax1.bar(selected_candidates, voix_totales_filtered, color=sns.color_palette("husl", len(selected_candidates)))
        ax1.set_xlabel("Candidates")  # Étiquette de l'axe des x
        ax1.set_ylabel("Total Votes")  # Étiquette de l'axe des y
        ax1.set_title("Votes by Selected Candidates")  # Titre du graphique
        plt.xticks(rotation=45, ha='right')  # Rotation des étiquettes des x pour améliorer la lisibilité
        st.pyplot(fig1)  # Affichage du graphique dans Streamlit

        # 2. Histogram of Taux de Participation - General view of registered voters
        st.title("Histogram - Distribution of Taux de Participation")
        # Calcul du taux de participation en pourcentage pour chaque commune
        df['Taux_participation'] = (df['Votants'] / df['Inscrits']) * 100
        fig2, ax2 = plt.subplots()
        # Création de l'histogramme avec des 20 bins et une courbe de densité KDE
        sns.histplot(df['Taux_participation'], bins=20, kde=True, ax=ax2)
        ax2.set_title('Distribution of Voter Turnout')  # Titre du graphique
        ax2.set_xlabel('Voter Turnout (%)')  # Étiquette de l'axe des x
        ax2.set_ylabel('Number of Communes')  # Étiquette de l'axe des y
        st.pyplot(fig2)

        # 3. Scatter plot: Registered voters vs Abstentions
        st.title("Scatter Plot - Registered Voters vs Abstentions")
        fig3, ax3 = plt.subplots()
        # Création d'un nuage de points avec les "Inscrits" sur l'axe des x et "Abstentions" sur l'axe des y
        ax3.scatter(df["Inscrits"], df["Abstentions"], color='blue', s=10, alpha=0.6)
        ax3.set_xlabel("Registered Voters")  # Étiquette de l'axe des x
        ax3.set_ylabel("Abstentions")  # Étiquette de l'axe des y
        ax3.set_title("Registered Voters vs Abstentions (Moderate Zoom)")  # Titre du graphique
        ax3.set_xlim(0, 10000)  # Limite de l'axe des x
        ax3.set_ylim(0, 3000)  # Limite de l'axe des y
        st.pyplot(fig3)

        # 4. Bar Chart: Voter Turnout by Department
        st.title("Bar Chart - Voter Turnout by Department")
        # Calcul du taux moyen de participation par département
        df_participation_dep = df.groupby(['code_departement', 'nom_departement'], as_index=False).agg({
            'Taux_participation': 'mean'
        }).sort_values(by='Taux_participation', ascending=False).head(10)

        fig4, ax4 = plt.subplots(figsize=(10, 6))
        # Création du graphique à barres avec les 10 départements ayant le taux de participation moyen le plus élevé
        sns.barplot(x='nom_departement', y='Taux_participation', data=df_participation_dep, ax=ax4)
        ax4.set_title('Voter Turnout by Department')  # Titre du graphique
        ax4.set_xlabel('Department')  # Étiquette de l'axe des x
        ax4.set_ylabel('Voter Turnout (%)')  # Étiquette de l'axe des y
        plt.xticks(rotation=45, ha='right')  # Rotation des étiquettes pour améliorer la lisibilité
        st.pyplot(fig4)

        # 5. Pie chart: Blank, Null, and Valid Votes
        st.title("Pie Chart - Votes")
        # Définitions des étiquettes et tailles pour les différentes catégories de votes
        labels = ["Blank Votes", "Invalid Votes", "Casted Votes"]
        sizes = [df["Blancs"].sum(), df["Nuls"].sum(), df["Exprimés"].sum()]

        fig5, ax5 = plt.subplots()
        # Création du diagramme circulaire (pie chart) avec les tailles des catégories de votes
        ax5.pie(sizes, startangle=90, colors=['skyblue', 'lightcoral', 'lightgreen'], autopct=None)
        total_votes = sum(sizes)  # Calcul du total des votes pour afficher les pourcentages
        # Création des étiquettes pour la légende
        legend_labels = [f"{label} - {size/total_votes*100:.1f}%" for label, size in zip(labels, sizes)]
        ax5.legend(legend_labels, loc="center left", bbox_to_anchor=(1, 0.5))  # Ajout de la légende
        ax5.axis('equal')  # Assurer que le diagramme est circulaire
        ax5.set_title("Votes", fontsize=14)  # Titre du graphique
        st.pyplot(fig5)

        # 6. Bar Chart: Votes by Department
        st.title("Bar Chart - Votes by Department")
        # Calcul du total des voix par département et tri décroissant par nombre de voix
        df_dep = df.groupby(['code_departement', 'nom_departement'], as_index=False).agg({'Voix': 'sum'}).sort_values(by='Voix', ascending=False)

        # Sélection des 10 départements avec le plus de voix
        top_10_dep = df_dep.head(10)

        fig6, ax6 = plt.subplots(figsize=(10, 6))
        # Création du graphique à barres pour les 10 départements ayant le plus de voix
        sns.barplot(x='code_departement', y='Voix', data=top_10_dep, palette="Blues_d", ax=ax6)
        ax6.set_title('Top Departments by Total Votes')  # Titre du graphique
        ax6.set_xlabel('Department Code')  # Étiquette de l'axe des x
        ax6.set_ylabel('Total Votes')  # Étiquette de l'axe des y
        plt.xticks(rotation=45, ha='right')  # Rotation des étiquettes des x
        st.pyplot(fig6)

        # 7. Display the top 10 departments
        # Affichage textuel des 10 départements avec le plus de voix
        st.markdown("### Top 10 Departments with the Most Votes")
        for idx, row in enumerate(top_10_dep.itertuples(), 1):
            st.write(f"{idx}. {row.nom_departement} (Code: {row.code_departement}) - {row.Voix} votes")

        # 8. Comparison of Votes by Candidate and Department (Top 20)
        st.title("Comparison of Votes by Candidate and Department (Top 20)")
        # Agrégation des voix par département et par candidat
        df_candidat_dep = df.groupby(['nom_departement', 'Nom']).agg({'Voix': 'sum'}).reset_index()

        # Calcul du total des voix par département et sélection des 20 départements ayant le plus de voix
        total_voix_dep = df.groupby('nom_departement').agg({'Voix': 'sum'}).reset_index()
        top_20_dep = total_voix_dep.sort_values(by='Voix', ascending=False).head(20)['nom_departement']

        # Filtrage des données pour ne garder que les départements du top 20
        df_candidat_dep_top20 = df_candidat_dep[df_candidat_dep['nom_departement'].isin(top_20_dep)]

        fig7, ax7 = plt.subplots(figsize=(12, 8))
        # Création d'un graphique à barres empilées comparant les voix par candidat dans le top 20 des départements
        sns.barplot(x='nom_departement', y='Voix', hue='Nom', data=df_candidat_dep_top20, ax=ax7, palette="Set2")

        ax7.set_title("Votes by Candidate in the Top 20 Departments")  # Titre du graphique
        ax7.set_xlabel("Department")  # Étiquette de l'axe des x
        ax7.set_ylabel("Total Votes")  # Étiquette de l'axe des y
        plt.xticks(rotation=45, ha='right')  # Rotation des étiquettes des x pour améliorer la lisibilité
        st.pyplot(fig7)

        #First Map: Sampled Communes
        st.title("Map of 500 Sampled Communes: Voter Turnout and Registered Voters 📍")

        # Nettoyage des données pour retirer les communes sans coordonnées géographiques (latitude et longitude)
        cleaned_commune_data = df.dropna(subset=['latitude', 'longitude'])

        # Nous sélectionnons un échantillon de 500 communes pour les afficher sur la carte afin de ne pas surcharger la carte
        sampled_communes = cleaned_commune_data.sample(n=500)

        # Création d'une carte centrée sur la France avec un niveau de zoom initial de 6
        commune_map = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

        # Boucle à travers chaque commune de l'échantillon pour ajouter des marqueurs à la carte
        for index, row in sampled_communes.iterrows():
            # Utilisation des coordonnées de la commune (latitude, longitude) pour placer un marqueur sur la carte
            # Chaque marqueur affiche un popup avec le nom de la commune, le taux de participation et le nombre d'inscrits
            folium.Marker(
                location=[row['latitude'], row['longitude']],  # Localisation de la commune sur la carte
                popup=f"Commune: {row['nom_commune_complet']}<br>Voter turnout: {row['Taux_participation']:.2f}%<br>Registered voters: {row['Inscrits']}",
                icon=folium.Icon(color='blue', icon='info-sign')  # Style du marqueur (bleu avec une icône d'information)
            ).add_to(commune_map)  # Ajout du marqueur à la carte

        # Affichage de la carte interactive avec les communes échantillonnées dans Streamlit
        folium_static(commune_map)

        # Second Map: Total Votes by Department
        st.title("Map 2: Total Votes by Department 📊")

        # Calcul du total des voix pour chaque département et regroupement des données par code de département et nom de département
        df_voix_par_departement = cleaned_commune_data.groupby(['code_departement', 'nom_departement']).agg({'Voix': 'sum'}).reset_index()

        # Sélection des 10 départements ayant obtenu le plus de voix
        top_10_departments = df_voix_par_departement.nlargest(10, 'Voix')

        # Création d'une carte centrée sur la France
        departments_map = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

        # Facteur d'échelle utilisé pour ajuster la taille des cercles proportionnels en fonction du nombre total de voix
        scaling_factor = 0.1  # Plus le facteur est grand, plus les cercles seront gros

        # Boucle à travers les 10 départements ayant obtenu le plus de voix
        for index, row in top_10_departments.iterrows():
            # Sélection d'une commune représentative du département pour utiliser ses coordonnées comme centre du cercle
            commune_in_dept = cleaned_commune_data[cleaned_commune_data['code_departement'] == row['code_departement']].iloc[0]

            # Ajout d'un cercle sur la carte, avec une taille proportionnelle au nombre total de voix dans le département
            folium.Circle(
                location=[commune_in_dept['latitude'], commune_in_dept['longitude']],  # Localisation centrale du département
                radius=row['Voix'] * scaling_factor,  # Taille du cercle proportionnelle au nombre total de voix
                color='crimson',  # Couleur du cercle
                fill=True,  # Le cercle est rempli de couleur
                fill_opacity=0.6,  # Opacité du remplissage (0 = transparent, 1 = opaque)
                popup=f"Department: {row['nom_departement']}<br>Total votes: {row['Voix']}"  # Informations affichées au survol
            ).add_to(departments_map)  # Ajout du cercle à la carte

        # Affichage de la carte interactive avec les cercles proportionnels dans Streamlit
        folium_static(departments_map)

        # Third Map: Clustered Communes
        st.title("Map 3: Clustered Communes 📍")

        # Création d'une carte interactive avec des clusters de marqueurs pour regrouper les communes proches
        cluster_map = folium.Map(location=[46.603354, 1.888334], zoom_start=6)

        # Ajout d'une fonctionnalité de cluster de marqueurs avec Folium
        marker_cluster = MarkerCluster().add_to(cluster_map)

        # Boucle à travers chaque commune (après nettoyage) pour ajouter des marqueurs aux clusters
        for index, row in cleaned_commune_data.iterrows():
            # Chaque commune est ajoutée avec ses coordonnées géographiques (latitude et longitude)
            # Un popup affiche le nom de la commune et le nombre total de voix pour cette commune
            folium.Marker(
                location=[row['latitude'], row['longitude']],  # Localisation de la commune
                popup=f"Commune: {row['nom_commune_complet']}<br>Votes: {row['Voix']}"  # Informations supplémentaires dans le popup
            ).add_to(marker_cluster)  # Ajout du marqueur au cluster

        # Affichage de la carte avec les clusters de communes dans Streamlit
        folium_static(cluster_map)

    else:
        # Message d'erreur si les données ne sont pas encore chargées
        st.error("The DataFrame has not been loaded yet. Please load the data in the 'Analysis' tab first.")
