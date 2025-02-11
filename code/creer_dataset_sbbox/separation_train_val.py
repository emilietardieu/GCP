from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
import shutil

def separer_train_val(images, gt_csv_path, output_dir, train_size=0.8, random_state=42):
    """
    Sépare les images en ensembles d'entraînement et de validation,
    et crée des fichiers CSV GT séparés pour chaque ensemble.

    Args:
        images (list): Liste des chemins des images (objets Path).
        gt_csv_path (Path): Chemin vers le fichier CSV des annotations (GT) contenant 'filename' et les keypoints.
        output_dir (Path): Dossier où les ensembles train/val seront créés.
        train_size (float): Proportion des données à utiliser pour l'ensemble d'entraînement.
        random_state (int): Graine pour le générateur de nombres aléatoires.

    Returns:
        None
    """

    # Charger le fichier GT complet
    gt_df = pd.read_csv(gt_csv_path)

    # Extraire uniquement les noms des fichiers pour la correspondance
    image_names = [img.name for img in images]  # .name pour obtenir seulement le nom du fichier

    # Séparer les images en train et validation
    images_train, images_val = train_test_split(image_names, train_size=train_size, random_state=random_state)

    # Créer les dossiers pour les images
    (output_dir / 'train/images').mkdir(parents=True, exist_ok=True)
    (output_dir / 'val/images').mkdir(parents=True, exist_ok=True)

    # Déplacement des images dans les dossiers correspondants
    for img in images:
        if img.name in images_train:
            shutil.move(str(img), str(output_dir / 'train/images' / img.name))
        else:
            shutil.move(str(img), str(output_dir / 'val/images' / img.name))

    # Filtrer les annotations GT pour chaque ensemble
    gt_train_df = gt_df[gt_df['filename'].isin(images_train)]
    gt_val_df = gt_df[gt_df['filename'].isin(images_val)]

    # Sauvegarder les fichiers GT pour train et val
    gt_train_df.to_csv(output_dir / 'train/images'/'gt_train.csv', index=False)
    gt_val_df.to_csv(output_dir / 'val'/'images'/'gt_val.csv', index=False)

    print(f"Images et annotations séparées avec succès dans '{output_dir}'.")

