import pandas as pd
from pathlib import Path
import random
import cv2
from tqdm import tqdm
import csv

def decouper_images_avec_keypoints(data, output_dir, csv_path, crop_size=512, overlap=0.1, prob_empty=0.05):
    """
    Découpe les images en sous-images avec chevauchement, ajoute des crops vides et sépare les keypoints en colonnes.
    """
    # Préparer le dossier de sortie
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Préparer le fichier CSV de sortie
    with open(csv_path, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([
            "image_originale", "crop_filename", "x_start", "y_start", "x_end", "y_end", 
            "x", "y", "x_relatif", "y_relatif", "total_keypoints"
        ])

        # Parcourir les données par 'path'
        for path, group in tqdm(data.groupby("nouveau_path")):
            # Charger l'image depuis le dossier 'images'
            image_path = Path(path)
            if not image_path.exists():
                print(f"Erreur : Fichier introuvable {image_path}")
                continue

            image = cv2.imread(str(image_path))
            if image is None:
                print(f"Erreur : Impossible de charger {image_path}")
                continue

            h, w, _ = image.shape
            step = int(crop_size * (1 - overlap))
            crop_count = 0

            # Créer un nom formaté pour l'image
            file_name = Path(path).name

            # Liste des keypoints pour cette image
            locations = [(row["x"], row["y"]) for _, row in group.iterrows()]

            # Découper l'image en crops
            for y in range(0, h, step):
                for x in range(0, w, step):

                    # Ajuster les bords si le crop dépasse les dimensions de l'image
                    x_end = min(x + crop_size, w)
                    y_end = min(y + crop_size, h)
                    x_start = x_end - crop_size if x_end == w else x
                    y_start = y_end - crop_size if y_end == h else y

                    # Filtrer les keypoints dans ce crop
                    crop_keypoints = [
                        (kx, ky) for kx, ky in locations
                        if x_start <= kx < x_end and y_start <= ky < y_end
                    ]

                    # Calculer les keypoints relatifs au crop
                    crop_keypoints_relatifs = [
                        (kx, ky, round(kx - x_start, 2), round(ky - y_start, 2)) for kx, ky in crop_keypoints
                    ]

                    # Nombre de keypoints dans ce crop
                    crop_total_keypoints = len(crop_keypoints)

                    # Générer un crop si keypoints présents ou avec probabilité pour les crops vides
                    if crop_keypoints or random.random() < prob_empty:
                        # Extraire le crop
                        crop = image[y_start:y_end, x_start:x_end]

                        # Nom du fichier pour le crop
                        crop_filename = f"{file_name}_crop_{crop_count:04d}.JPG"
                        crop_path = output_dir / crop_filename

                        # Sauvegarder le crop
                        cv2.imwrite(str(crop_path), crop)

                        # Sauvegarder les métadonnées
                        if crop_keypoints:
                            for kx, ky, kx_rel, ky_rel in crop_keypoints_relatifs:
                                csv_writer.writerow([
                                    image_path.name,
                                    crop_filename,
                                    x_start, y_start, x_end, y_end,
                                    kx, ky, kx_rel, ky_rel,
                                    crop_total_keypoints  # Nombre de keypoints pour ce crop
                                ])
                        else:
                            # Sauvegarder les crops sans keypoints
                            csv_writer.writerow([
                                image_path.name,
                                crop_filename,
                                x_start, y_start, x_end, y_end,
                                "", "", "", "",  # Pas de keypoints
                                crop_total_keypoints  # Nombre de keypoints dans ce crop (0)
                            ])

                        crop_count += 1

            print(f"{crop_count} sous-images générées pour {image_path}")



# Charger le CSV contenant les keypoints
data = pd.read_csv("/home/hiphen/Documents/GCP/data/my_data/filtered_data/advanta_csv.csv", sep = ";")  

# Ajuster le chemin des images
base_image_dir = "/home/hiphen/Documents/GCP/data/my_data/Resize_data/images_originales"  # Dossier réel des images

# Appeler la fonction
output_dir = "/home/hiphen/Documents/GCP/data/my_data/Resize_data/cropped_images"
csv_output = "/home/hiphen/Documents/GCP/data/my_data/Resize_data/sous_images_metadata.csv"
decouper_images_avec_keypoints(data, output_dir, csv_output)
