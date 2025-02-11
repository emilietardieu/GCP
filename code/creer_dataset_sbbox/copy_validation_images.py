# recupère les imùages du cropped_images a partir d'un fichier gt.csv (pour la validation)
import os
import pandas as pd
import shutil

def copy_validation_images(csv_path, cropped_images_dir, output_dir):
    """
    Copie les images listées dans le CSV depuis 'cropped_images' vers 'images_validations'.

    :param csv_path: Chemin vers le fichier CSV contenant les noms des images dans la colonne 'filename'.
    :param cropped_images_dir: Dossier contenant les images recadrées.
    :param output_dir: Dossier où les images de validation seront copiées.
    """

    # Charger le CSV et récupérer les noms des fichiers
    df = pd.read_csv(csv_path)
    image_filenames = df['filename'].tolist()

    # Créer le dossier de sortie s'il n'existe pas
    os.makedirs(output_dir, exist_ok=True)

    # Parcourir les noms d'images et copier celles qui existent
    for filename in image_filenames:
        # Extraire le nom de fichier (sans le chemin complet)
        image_name = os.path.basename(filename)

        # Chemin complet de l'image source et de destination
        source_path = os.path.join(cropped_images_dir, image_name)
        destination_path = os.path.join(output_dir, image_name)

        # Vérifie si l'image existe dans 'cropped_images' avant de copier
        if os.path.exists(source_path):
            shutil.copy2(source_path, destination_path)
            print(f"Image copiée : {image_name}")
        else:
            print(f"Image non trouvée dans '{cropped_images_dir}': {image_name}")

# Exemple d'utilisation
csv_path = '/home/hiphen/Documents/GCP/data/my_data/Test_data/toutes_les_images/validation/validation_images.csv'
cropped_images_dir = '/home/hiphen/Documents/GCP/data/my_data/Test_data/toutes_les_images/images_cropped'
output_dir = '/home/hiphen/Documents/GCP/data/my_data/Test_data/toutes_les_images/validation/images'

copy_validation_images(csv_path, cropped_images_dir, output_dir)
