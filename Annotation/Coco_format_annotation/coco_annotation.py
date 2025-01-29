import json
import pandas as pd
from pathlib import Path
from PIL import Image
from tqdm import tqdm

# Chemins des fichiers
csv_path = Path(r"/home/hiphen/Documents/GCP/data/my_data/filtered_data/data_filtered_jpg.csv")

images_dir_train = Path(r"/home/hiphen/Documents/GCP/data/my_data/coco/train")
images_dir_val = Path(r"/home/hiphen/Documents/GCP/data/my_data/coco/val")

output_json_train = Path(r"/home/hiphen/Documents/GCP/data/my_data/coco/annotations/keypoints_train_test.json")
output_json_val = Path(r"/home/hiphen/Documents/GCP/data/my_data/coco/annotations/keypoints_val_test.json")

# Charger les données CSV
data = pd.read_csv(csv_path, sep=";")

# Fonction pour créer un fichier JSON COCO
def create_coco_json(images_dir, data_subset, output_json_path):
    # Initialiser la structure COCO
    coco_format = {
        "images": [],
        "annotations": [],
        "categories": [{"id": 1, "name": "GCP"}]
    }

    # Remplir les données
    for i, row in tqdm(data_subset.iterrows(), total=data_subset.shape[0]):
        # Extraire uniquement le nom du fichier
        file_name = Path(row["camera"]).name

        # Chemin complet de l'image
        image_path = images_dir / file_name

        # Récupérer les dimensions de l'image avec Pillow
        if image_path.exists():
            with Image.open(image_path) as img:
                width, height = img.size

            # Ajouter les images
            image_id = i + 1
            keypoint_id = i + 1

            coco_format["images"].append({
                "id": image_id,
                "file_name": file_name,
                "width": width,
                "height": height
            })

            # Générer les informations supplémentaires
            x, y = row["x"], row["y"]

            width, height = 10, 10  # Dimensions du rectangle

            x_min = x - width / 2
            y_min = y - height / 2

            segmentation = [
                x_min, y_min,               # Coin supérieur gauche
                x_min + width, y_min,       # Coin supérieur droit
                x_min + width, y_min + height,  # Coin inférieur droit
                x_min, y_min + height       # Coin inférieur gauche
            ]

            bbox = [x - width / 2, y - height / 2, width, height] 

            # Ajouter les annotations
            keypoints = [x, y, 2]  # Coordonnées (x, y), visibilité
            area = bbox[2] * bbox[3]  # Largeur * hauteur
            coco_format["annotations"].append({
                "id": keypoint_id,
                "image_id": image_id,
                "category_id": 1,
                "keypoints": keypoints,
                "num_keypoints": 1,
                "segmentation": [segmentation],
                "area": area,
                "bbox": bbox,
                "iscrowd": 0 , # Toujours 0 si ce n'est pas une annotation groupée
                "input_center" : 1
            })

    # Sauvegarder le fichier JSON
    with open(output_json_path, "w") as f:
        json.dump(coco_format, f, indent=4)

    print(f"Fichier JSON créé : {output_json_path}")

# Générer les fichiers JSON pour train et val
create_coco_json(images_dir_train, data, output_json_train)
create_coco_json(images_dir_val, data, output_json_val)
