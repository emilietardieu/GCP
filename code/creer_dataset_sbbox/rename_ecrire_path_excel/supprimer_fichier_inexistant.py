from pathlib import Path
import pandas as pd
# PosixPath('/media/nas-production/inrae_toulouse/toulouse_2023_av/AV/cims_on_tournesol/2023-07-20/dataset/DJI_20230720104751_0077.JPG')

def suppr_path(chemin_inexistant, fichier_csv):
    
    colonne_chemins = "path"

    # Charger le fichier CSV
    df = pd.read_csv(fichier_csv, sep=";")
# Traiter les chemins inexistants pour correspondre au format dans le CSV
    chemins_a_supprimer = []
    print("chemins inex",chemin_inexistant)
    for chemin in chemin_inexistant:
        # Remplacer les préfixes pour gérer les variations
        chemin_o_upper = Path(str(chemin).replace("/media/nas-production", "O:").replace("/media/nas-archives", "O:"))
        chemin_o_lower = Path(str(chemin).replace("/media/nas-production", "o:").replace("/media/nas-archives", "o:"))

        # Ajouter les deux variantes (O: et o:) pour la comparaison
        chemins_a_supprimer.append(str(chemin_o_upper))
        chemins_a_supprimer.append(str(chemin_o_lower))

    # Supprimer les doublons éventuels dans la liste
    chemins_a_supprimer = list(set(chemins_a_supprimer))

    # Filtrer les lignes dans le DataFrame
    df = df[~df[colonne_chemins].isin(chemins_a_supprimer)]

    # Sauvegarder le fichier CSV modifié
    df.to_csv(fichier_csv, sep=";", index=False)
    print(f"{len(chemins_a_supprimer)} variations de chemins vérifiées. Fichier CSV mis à jour.")