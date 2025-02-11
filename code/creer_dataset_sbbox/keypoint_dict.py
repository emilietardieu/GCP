import pandas as pd
from pathlib import Path
import random
import cv2
from tqdm import tqdm
import csv

def decouper_images_avec_keypoints(fichier_csv, output_dir, csv_path, crop_size=1024, prob_empty=0, resize_factor_avant=2, resize_factor_apres=4, overlap=0.3):
    """
    Découpe les images en sous-images avec un chevauchement, réduit leur résolution et gère les keypoints.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(fichier_csv, sep = ";")  

    with open(csv_path, mode='w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([
            "image_originale", "crop_filename", "x_start", "y_start", "x_end", "y_end", 
            "x", "y", "x_relatif", "y_relatif", "total_keypoints"
        ])

        for path, group in tqdm(data.groupby("nouveau_path")):
            image_path = Path(path)
            if not image_path.exists():
                print(f"Erreur : Fichier introuvable {image_path}")
                continue

            image = cv2.imread(str(image_path))
            if image is None:
                print(f"Erreur : Impossible de charger {image_path}")
                continue

            # Réduction de la résolution avant le cropping
            h, w, _ = image.shape
            image = cv2.resize(image, (int(w / resize_factor_avant), int(h / resize_factor_avant)))
            h, w, _ = image.shape

            file_name = Path(path).name
            locations = [(round(row["x"] / resize_factor_avant, 2), round(row["y"] / resize_factor_avant, 2)) for _, row in group.iterrows()]

            crop_count = 0
            keypoint_crop_saved = False
            step = int(crop_size * (1 - overlap))
            for y_start in range(0, h - crop_size + 1, step):
                for x_start in range(0, w - crop_size + 1, step):
                    x_end = x_start + crop_size
                    y_end = y_start + crop_size

                    crop_keypoints = [(kx, ky) for kx, ky in locations if x_start <= kx < x_end and y_start <= ky < y_end]
                    crop_keypoints_relatifs = [(kx, ky, round((kx - x_start) / resize_factor_apres, 2), round((ky - y_start) / resize_factor_apres, 2)) for kx, ky in crop_keypoints]
                    crop_total_keypoints = len(crop_keypoints)

                    if not keypoint_crop_saved and crop_keypoints:
                        keypoint_crop_saved = True
                    elif keypoint_crop_saved and crop_keypoints:
                        continue
                    
                    if not crop_keypoints and random.random() >= prob_empty:
                        continue
                    
                    crop = image[y_start:y_end, x_start:x_end]
                    
                    # Réduction de la résolution après le cropping
                    crop = cv2.resize(crop, (int(crop_size / resize_factor_apres), int(crop_size / resize_factor_apres)))
                    
                    crop_filename = f"{file_name}_crop_{crop_count:04d}.JPG"
                    crop_path = output_dir / crop_filename
                    cv2.imwrite(str(crop_path), crop)

                    if crop_keypoints:
                        for kx, ky, kx_rel, ky_rel in crop_keypoints_relatifs:
                            csv_writer.writerow([
                                image_path.name, crop_filename, round(x_start, 2), round(y_start, 2), round(x_end, 2), round(y_end, 2),
                                round(kx, 2), round(ky, 2), round(kx_rel, 2), round(ky_rel, 2), crop_total_keypoints
                            ])
                    else:
                        csv_writer.writerow([
                            image_path.name, crop_filename, round(x_start, 2), round(y_start, 2), round(x_end, 2), round(y_end, 2),
                            "", "", "", "", crop_total_keypoints
                        ])
                    crop_count += 1
            print(f"{crop_count} sous-images générées pour {image_path}")