import json
import pandas as pd
from pathlib import Path
from tqdm import tqdm


def create_gt_csv(csv_metadata, output_csv_path):
    
    data_subset = pd.read_csv(csv_metadata, sep=",")

    # Liste pour stocker les informations formatées
    csv_data = []

    # Parcourir les données par 'image_originale'
    for image_originale, group in tqdm(data_subset.groupby("crop_filename")):
        # Liste des noms des crops
        crop_filenames = group["crop_filename"].tolist()
        crop_filenames = crop_filenames[0]

        # Liste des keypoints relatifs sous forme de tuples
        locations = [(row["y_relatif"], row["x_relatif"]) for _, row in group.iterrows() if not pd.isna(row["x_relatif"])]


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


