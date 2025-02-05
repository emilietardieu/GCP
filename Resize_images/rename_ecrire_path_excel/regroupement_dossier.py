import pandas as pd
from pathlib import Path
from tqdm import tqdm
from regrouper_images_fonction import regrouper_dossiers_images
from supprimer_fichier_inexistant import suppr_path


# Chargement du fichier CSV 
fichier_csv = Path(r"/home/hiphen/Documents/GCP/data/my_data/filtered_data/advanta_csv.csv")

colonne_chemins = 'path'

# Lire les chemins depuis le fichier CSV
df = pd.read_csv(fichier_csv, sep=";")
print(df.columns)
chemins_images = df[colonne_chemins].dropna()

# Initialiser une nouvelle colonne pour les nouveaux chemins
df['nouveau_path'] = None
print(df.columns)
# Extraire les dossiers uniques
dossier_destination = set(Path(chemin).parent for chemin in chemins_images)

chemin_inexistant = set()

# Dossier cible où regrouper les images
dossier_cible = Path(r"/home/hiphen/Documents/GCP/data/my_data/Resize_data/advanta/images_originales")

# Parcourir les images et mettre à jour les chemins
tqdm_desc = "\nParcours des dossiers"
for index, chemin_image in enumerate(tqdm(chemins_images, desc=tqdm_desc)):
    chemin_image = Path(str(chemin_image).replace("O:", "/media/nas-production"))
    chemin_image = Path(str(chemin_image).replace("o:", "/media/nas-production"))
    
    chemin_image_destination = regrouper_dossiers_images(chemin_image, dossier_cible, fichier_csv)
    
    if chemin_image_destination == False:
        chemin_inexistant.add(chemin_image)
    else:
        # Ajouter le chemin de destination dans la colonne 'nouveau_path'
        df.at[index, 'nouveau_path'] = str(chemin_image_destination)

# Trier les chemins inexistants et mettre à jour le CSV
chemin_inexistant = sorted(chemin_inexistant)
suppr_path(chemin_inexistant, fichier_csv)

# Sauvegarder les mises à jour dans le fichier CSV
df.to_csv(fichier_csv, sep=";", index=False)