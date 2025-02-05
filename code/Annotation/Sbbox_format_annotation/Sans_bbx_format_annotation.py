import json
import pandas as pd
from pathlib import Path
from tqdm import tqdm

# Chemin du fichier d'entrée et du fichier de sortie
csv_path = Path(r"/home/hiphen/Documents/GCP/data/my_data/filtered_data/advanta_csv.csv")
output_file = Path(r"/home/hiphen/Documents/GCP/data/my_data/sbbox_test/gt.csv")

# Charger les données CSV
data = pd.read_csv(csv_path, sep=";")

def create_gt_csv(data_subset, output_csv_path):
    # Liste pour stocker les informations formatées
    csv_data = []

    # Parcourir les données par 'path'
    for path, group in tqdm(data_subset.groupby("path")):
        file_name = Path(path).as_posix().replace("/", "_").replace("_media_nas-production", "").replace("O:_", "").replace("_RGB", "").replace("_dataset", "").replace("_AV", "").replace("_image_undistort", "")

        # Créer la liste des locations sous forme de tuples
        locations = [(row["x"], row["y"]) for _, row in group.iterrows()]
        
        # Ajouter les informations formatées à la liste
        csv_data.append({
            "filename": file_name,
            "count": len(locations),
            "locations": str(locations)
        })

    # Créer le fichier CSV final
    pd.DataFrame(csv_data).to_csv(output_csv_path, index=False)

# Générer le fichier CSV
create_gt_csv(data, output_file)

print(f"Fichier '{output_file}' généré avec succès.")