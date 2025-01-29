from pathlib import Path
import cv2
import csv
import random

def decouper_images_avec_overlap(input_dir, output_dir, csv_path, keypoints_dict, crop_size=1024, overlap=0.05):
    """
    Découpe des images en sous-images avec chevauchement. Filtre selon les keypoints et limite le nombre de crops.
    
    :param input_dir: Dossier contenant les images d'origine.
    :param output_dir: Dossier où sauvegarder les sous-images.
    :param csv_path: Fichier CSV pour enregistrer les métadonnées.
    :param keypoints_dict: Dictionnaire avec les keypoints {nom_image: [(x1, y1), (x2, y2), ...]}.
    :param crop_size: Taille des crops.
    :param overlap: Chevauchement entre crops (entre 0 et 1).
    """
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    step = int(crop_size * (1 - overlap))

    with open(csv_path, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["image_originale", "filename", "x_start", "y_start", "x_end", "y_end", "keypoints"])

        for image_path in input_dir.glob("*.*"):
            image = cv2.imread(str(image_path))
            if image is None:
                print(f"Erreur : Impossible de charger {image_path}")
                continue

            h, w, _ = image.shape
            crop_count = 0

            # Récupérer les keypoints pour cette image
            keypoints = keypoints_dict.get(image_path.name, [])

            for y in range(0, h - crop_size + 1, step):
                for x in range(0, w - crop_size + 1, step):

                    # Coordonnées du crop
                    crop_coords = (x, y, x + crop_size, y + crop_size)

                    # Vérifier si le crop contient des keypoints
                    if contient_keypoints(crop_coords, keypoints) or random.random() < 0.25:
                        crop = image[y:y + crop_size, x:x + crop_size]
                        crop_filename = f"{image_path.stem}_crop_{crop_count:04d}.png"
                        crop_path = output_dir / crop_filename
                        cv2.imwrite(str(crop_path), crop)

                        # Sauvegarder les métadonnées
                        crop_keypoints = [
                            (kx, ky) for kx, ky in keypoints
                            if x <= kx < x + crop_size and y <= ky < y + crop_size
                        ]
                        csv_writer.writerow([
                            image_path.name,
                            crop_filename,
                            x, y, x + crop_size, y + crop_size,
                            crop_keypoints
                        ])
                        crop_count += 1

            print(f"{crop_count} sous-images générées pour {image_path.name}")

def contient_keypoints(crop_coords, keypoints):
    """
    Vérifie si des keypoints sont présents dans un crop.
    """
    x_start, y_start, x_end, y_end = crop_coords
    for keypoint in keypoints:
        x, y = keypoint
        if x_start <= x < x_end and y_start <= y < y_end:
            return True
    return False


input_dir = "/home/hiphen/Documents/GCP/data/my_data/Resize_data/images_originales"
output_dir = "/home/hiphen/Documents/GCP/data/my_data/Resize_data/croppeds_images"
csv_path = "/home/hiphen/Documents/GCP/data/my_data/Resize_data/sous_images_metadata.csv"

