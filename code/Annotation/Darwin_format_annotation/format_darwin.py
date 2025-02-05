from info_image import *
import uuid
import json
from pathlib import Path

output_dir = Path(r"/home/hiphen/Documents/GCP/data/my_data/darwin_json")

def create_darwin_json_for_image(image, dataset_name, team_name, dataset_slug, team_slug):
    item_id = str(uuid.uuid4())

    annotations = []  
    for i in range(len(image["annotations"])):
        annotations.append({
            "id": str(uuid.uuid4()),
            "keypoint": {
                "x": image["annotations"][i]["x"],
                "y": image["annotations"][i]["y"]
            },
            "name": "GCP_Center",
            "properties": [],
            "slot_names": ["0"]
        })

    path_entier = Path(image["path_entier"])
    chemin_relatif = Path(*path_entier.parts[1:]).parent
    chemin_relatif = Path(chemin_relatif).parent
    chemin_relatif = str(chemin_relatif).replace("AV/", "").replace("RGB","")

    darwin_structure = {
        "version": "2.0",
        "schema_ref": "https://darwin-public.s3.eu-west-1.amazonaws.com/darwin_json/2.0/schema.json",
        "item": {
            "name": image["name"],
            "path": str(chemin_relatif),
            "source_info": {
                "item_id": item_id,
                "dataset": {
                    "name": dataset_name,
                    "slug": dataset_slug,
                    "dataset_management_url": f"https://darwin.v7labs.com/datasets/{dataset_slug}/dataset-management"
                },
                "team": {
                    "name": team_name,
                    "slug": team_slug
                },
                "workview_url": f"https://darwin.v7labs.com/workview?dataset={dataset_slug}&item={item_id}"
            },
            "slots": [
                {
                    "type": "image",
                    "slot_name": "0",
                    "width": image["width"],
                    "height": image["height"],
                    "thumbnail_url": image["thumbnail_url"],
                    "source_files": [
                        {
                            "file_name": image["name"],
                            "url": image["url"]
                        }
                    ]
                }
            ]
        },
        "annotations": annotations ,
        "properties": []
    }
    return darwin_structure

dataset_name = "GCP"
team_name = "Hiphen"
dataset_slug = "gcp"
team_slug = "hiphen"

# Créer le répertoire de sortie s'il n'existe pas
output_dir.mkdir(parents=True, exist_ok=True)

images_info = create_info_images(images_dir, data)

for image in images_info:
    # Générer les données Darwin pour l'image
    darwin_data = create_darwin_json_for_image(image, dataset_name, team_name, dataset_slug, team_slug)

    # Obtenir le chemin relatif en ignorant les 3 premiers dossiers
    path_entier = Path(image["path_entier"])
    chemin_relatif = Path(*path_entier.parts[1:])  # Ignorer les 3 premiers niveaux (racine)
    output_subdir = output_dir / chemin_relatif.parent  # Conserver l'arborescence relative sans les 3 premiers dossiers

    # Créer le sous-dossier si nécessaire
    output_subdir.mkdir(parents=True, exist_ok=True)

    # Nom du fichier JSON dans le sous-dossier
    json_file_name = output_subdir / f"{path_entier.stem}.json"

    # Écrire le fichier JSON
    with open(json_file_name, "w") as f:
        json.dump(darwin_data, f, indent=2)

print(f"Fichiers JSON créés dans : {output_dir}")