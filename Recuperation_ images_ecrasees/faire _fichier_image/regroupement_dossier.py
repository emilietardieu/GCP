import pandas as pd
from pathlib import Path
from tqdm import tqdm
from regrouper_images_fonction import regrouper_dossiers_images
from supprimer_fichier_inexistant import suppr_path



# Chargement du fichier CSV 
fichier_csv = Path(r"/home/hiphen/Documents/GCP/data/my_data/filtered_data/data_filtered_jpg.csv")
colonne_chemins = 'path'

# Lire les chemins depuis le fichier CSV
df = pd.read_csv(fichier_csv, sep=";")
print(df.columns)
chemins_images = df[colonne_chemins].dropna()

# Extraire les dossiers uniques
dossier_destination = set(Path(chemin).parent for chemin in chemins_images)

chemin_inexistant = set()

# Dossier cible où regrouper les dossiers contenant des images
dossier_cible = Path(r"/home/hiphen/Documents/GCP/data/my_data/images")

# Parcourir les images 
for chemin_image in tqdm(chemins_images, desc="\nParcours des dossiers"):
    chemin_image = Path(str(chemin_image ).replace("O:", "/media/nas-production"))
    chemin_image = Path(str(chemin_image ).replace("o:", "/media/nas-production"))
    image_existe = regrouper_dossiers_images(chemin_image , dossier_cible)
    if image_existe == False : 
        chemin_inexistant.add(chemin_image)


chemin_inexistant = sorted(chemin_inexistant)
suppr_path(chemin_inexistant, fichier_csv)





