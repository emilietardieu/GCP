
import shutil
from tqdm import tqdm
from pathlib import Path

# Chemin du dossier source contenant les images
source_folder = Path(r"R:\MACHINE_LEARNING\DATASETS\GCP\images")

# Liste des fichiers dans le dossier source
file_list = source_folder.glob("*.JPG") # `glob` permet de rechercher des fichiers correspondant à un motif donné (*.JPG)

# Chemin du nouveau dossier pour les fichiers JPEG
destination_folder = Path(r"D:\GCP\data\my_data\filtered_data\filtered_images")

# Crée le dossier de destination s'il n'existe pas
# `mkdir` crée le répertoire avec l'option `parents=True` pour créer tous les répertoires parents manquants
# `exist_ok=True` évite une erreur si le dossier existe déjà
destination_folder.mkdir(exist_ok=True, parents=True)

# Parcourt tous les fichiers dans le dossier source
for filename in tqdm(file_list, desc="Filtrage des fichiers JPEG"):
    destination_path = destination_folder.joinpath(filename.name)
    shutil.copy(filename, destination_path)

print(f"Les fichiers JPEG ont été copiés dans {destination_folder}")
