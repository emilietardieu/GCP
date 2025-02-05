import json
import pandas as pd
from pathlib import Path
from tqdm import tqdm

# Chemin du fichier d'entrée et du fichier de sortie

#  Toutes les images (14 500)
# csv_path = Path(r"/home/hiphen/Documents/GCP/data/my_data/sbbox/sous_images_metadata.csv")
# output_file = Path(r"/home/hiphen/Documents/GCP/data/my_data/sbbox/images_cropped/gt.csv")

#  Test avec les images advanta (1500)
csv_path = Path(r"/home/hiphen/Documents/GCP/data/my_data/Resize_data/advanta/sans_0/images_256x256/sous_images_metadata.csv")
output_file = Path(r"/home/hiphen/Documents/GCP/data/my_data/Resize_data/advanta/sans_0/images_256x256/images_cropped_sans0_256x256/gt.csv")

#  Test avec 10 images
# csv_path = Path(r"/home/hiphen/Documents/GCP/data/my_data/Resize_data/10_echantillons/sous_images_metadata.csv")
# output_file = Path(r"/home/hiphen/Documents/GCP/data/my_data/Resize_data/10_echantillons/images_cropped/gt.csv")

# #  Test avec 80 images
# csv_path = Path(r"/home/hiphen/Documents/GCP/data/my_data/Resize_data/10_echantillons/images_a_tester2/sous_images_metadata.csv")
# output_file = Path(r"/home/hiphen/Documents/GCP/data/my_data/Resize_data/10_echantillons/images_a_tester2/images_cropped/gt.csv")

# Charger les données CSV
data = pd.read_csv(csv_path, sep=",")

def create_gt_csv(data_subset, output_csv_path):
    # Liste pour stocker les informations formatées
    csv_data = []

    # Parcourir les données par 'image_originale'
    for image_originale, group in tqdm(data_subset.groupby("crop_filename")):
        # Liste des noms des crops
        crop_filenames = group["crop_filename"].tolist()
        crop_filenames = crop_filenames[0]

        # Liste des keypoints relatifs sous forme de tuples
        locations = [(row["x_relatif"], row["y_relatif"]) for _, row in group.iterrows() if not pd.isna(row["x_relatif"])]


        # Nombre total de keypoints pour ce crop
        count = len(locations)

        # Ajouter les informations formatées à la liste
        csv_data.append({
            "filename": crop_filenames,  # Un seul crop à la fois
            "count": count,
            "locations":  json.dumps(locations)
        })

    # Créer le fichier CSV final
    pd.DataFrame(csv_data).to_csv(output_csv_path, index=False, sep=",")

# Générer le fichier CSV
create_gt_csv(data, output_file)

print(f"Fichier '{output_file}' généré avec succès.")
