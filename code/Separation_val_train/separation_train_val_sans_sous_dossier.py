import shutil
from pathlib import Path
from tqdm import tqdm
from sklearn.model_selection import train_test_split

# Chemins
images_dir = Path(r"/home/hiphen/Documents/GCP/data/my_data/Reorganisation_regroupement_images_ecrasees/O:_inrae_montpellier_inrae_pommiers_2023_AV_Mauguio_2023-04-26_dataset")
output_dir = Path(r"/home/hiphen/Documents/GCP/data/my_data/coco")
train_dir = output_dir / "train"
val_dir = output_dir / "val"

# Créer les dossiers train et val s'ils n'existent pas
train_dir.mkdir(parents=True, exist_ok=True)
val_dir.mkdir(parents=True, exist_ok=True)

# Récupérer toutes les images dans le dossier principal
all_images = list(images_dir.glob("*.*"))  # Prend tous les fichiers peu importe l'extension

# Vérification des images trouvées
if not all_images:
    raise ValueError("Aucune image trouvée dans le dossier spécifié.")

# Fractionner les images en 80% pour train et 20% pour val
train_images, val_images = train_test_split(all_images, test_size=0.2, random_state=42)

# Copier les images pour le dossier train
for img_path in tqdm(train_images, desc="train images"):
    shutil.copy(str(img_path), train_dir / img_path.name)

# Copier les images pour le dossier val
for img_path in tqdm(val_images, desc="val images"):
    shutil.copy(str(img_path), val_dir / img_path.name)

print(f"Images copiées : {len(train_images)} dans 'train/', {len(val_images)} dans 'val/'.")
