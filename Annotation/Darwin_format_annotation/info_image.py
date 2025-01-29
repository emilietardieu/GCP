import json
import pandas as pd
from pathlib import Path
from PIL import Image
from tqdm import tqdm

# Chemins des fichiers
csv_path = Path(r"/home/hiphen/Documents/GCP/data/my_data/filtered_data/data_filtered_jpg.csv")
images_dir = Path(r"/home/hiphen/Documents/GCP/data/my_data/images")

# Charger les données CSV
data = pd.read_csv(csv_path, sep=";")

def create_info_images(images_dir, data_subset):
    images_info = []  # Utilisation d'une liste au lieu d'un dictionnaire

    # Créer une liste de tous les fichiers d'images dans le dossier
    all_images = list(images_dir.rglob("*"))  # Parcours récursif
    
    for path, group in tqdm(data_subset.groupby("path")):  # Regrouper les lignes par `path`
        file_name = Path(path).name

        # Rechercher l'image correspondante
        matching_image = next((img for img in all_images if img.name == file_name), None)

        if matching_image and matching_image.exists():
            with Image.open(matching_image) as img:
                width, height = img.size

            path_dossier = str(Path(path).parent)
            #path_dossier = "_" + str(Path(path_dossier)).replace("O:/", "").replace("/", "_")
            path_dossier = str(Path(path_dossier)).replace("O:/", "").replace("/", "_")

            # Construire l'entrée pour l'image
            image_info = {
                "name": file_name,
                "path_entier": path,
                "path_dossier" : path_dossier,
                "width": width,
                "height": height,
                "thumbnail_url": "https://example.com/thumbnail.jpg",
                "url": "https://example.com/image.jpg",
                "annotations": [
                    {"x": row["x"], "y": row["y"]} for _, row in group.iterrows()
                ],
            }
            
            images_info.append(image_info)

    # print(f"Fichier JSON créé : {output_json_path}")
    return images_info

# Exemple d'utilisation
images_info = create_info_images(images_dir, data)
