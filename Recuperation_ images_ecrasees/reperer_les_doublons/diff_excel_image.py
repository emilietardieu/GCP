import pandas as pd
from pathlib import Path

def comparer_dossier_et_excel(dossier_images, fichier_csv, colonne_chemins):
    """
    Compare un dossier d'images avec les chemins listés dans un fichier Excel (CSV).
    
    Args:
        dossier_images (str): Chemin du dossier contenant les images.
        fichier_csv (str): Chemin du fichier CSV contenant les chemins.
        colonne_chemins (str): Nom de la colonne contenant les chemins dans le CSV.
    
    Returns:
        dict: Dictionnaire contenant les résultats :
              - "images_non_listees": Images présentes dans le dossier mais absentes dans le CSV.
              - "chemins_inexistants": Chemins présents dans le CSV mais absents dans le dossier.
    """
    # Charger les chemins du CSV
    df = pd.read_csv(fichier_csv, sep=";")
    chemins_excel = df[colonne_chemins].dropna().apply(lambda x: Path(x.strip().replace("/", "_")))

    # Liste des images dans le dossier
    dossier_images = Path(dossier_images)
    images_dossier = list(dossier_images.rglob("*"))  # Inclut tous les fichiers dans le dossier et sous-dossiers

    # Trouver les images présentes dans le dossier mais absentes dans le CSV
    images_dossier_set = list(
    str(img.relative_to(dossier_images)).replace("/", "_")  # Chemin relatif à dossier_images
    for img in images_dossier if img.is_file()
)
    chemins_excel_set = list(str(chemin) for chemin in chemins_excel)

    print("nbr element excel",len(chemins_excel_set))
    print("nbr images",len(images_dossier_set))


    # images_non_listees = images_dossier_set - chemins_excel_set

    # Trouver les chemins présents dans le CSV mais dont les images sont absentes dans le dossier
    # chemins_inexistants = chemins_excel_set - images_dossier_set

    return len(chemins_excel_set) == len(images_dossier_set)


# Chemins à comparer
dossier_images = "/home/hiphen/Documents/GCP/data/my_data/Reorganisation_regroupement_images_ecrasees"
fichier_csv = "/home/hiphen/Documents/GCP/data/my_data/filtered_data/data_filtered_jpg.csv"
colonne_chemins = "path"

# Appeler la fonction pour comparer
resultats = comparer_dossier_et_excel(dossier_images, fichier_csv, colonne_chemins)
print(resultats)

# # Afficher les résultats
# print(f"Images non listées dans l'Excel : {len(resultats['images_non_listees'])}")
# for image in resultats["images_non_listees"]:
#     print(image)

# print(f"\nChemins inexistants dans le dossier : {len(resultats['chemins_inexistants'])}")
# # for chemin in resultats["chemins_inexistants"]:
# #     print(chemin)
