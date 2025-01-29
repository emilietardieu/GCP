import json
import pandas as pd
from pathlib import Path
from tqdm import tqdm

# Chemin du fichier d'entrée et du fichier de sortie
csv_path = Path(r"/home/hiphen/Documents/GCP/data/my_data/Resize_data/sous_images_metadata.csv")
output_file = Path(r"/home/hiphen/Documents/GCP/data/my_data/Resize_data/cropped_images/gt.csv")

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
            "locations": locations # Liste de tuples formatée avec des guillemets
        })

    # Créer le fichier CSV final
    pd.DataFrame(csv_data).to_csv(output_csv_path, index=False, sep=",")

# Générer le fichier CSV
create_gt_csv(data, output_file)

print(f"Fichier '{output_file}' généré avec succès.")
