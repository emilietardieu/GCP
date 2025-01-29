import shutil
from pathlib import Path
from tqdm import tqdm

def copy_image_with_progress(chemin_image, dossier_destination):
    """
    Copie une image dans un dossier cible avec une barre de progression.

    Args:
        chemin_image (Path): Chemin complet de l'image à copier.
        dossier_destination (Path): Dossier de destination.
    """
    chemin_image = Path(chemin_image)
    dossier_destination = Path(dossier_destination)

    # Vérifier si l'image existe
    if not chemin_image.exists() or not chemin_image.is_file():
        print(f"Fichier introuvable ou non valide : {chemin_image}")
        return False

    # Créer le dossier de destination si nécessaire
    if not dossier_destination.exists():
        dossier_destination.mkdir(parents=True, exist_ok=True)

    # Préparer la copie
    total_files = 1
    destination_path = dossier_destination / chemin_image.name

    with tqdm(total=total_files, desc=f"Copie de {chemin_image.name}", unit="fichier") as pbar:
        # Copier l'image
        shutil.copy2(chemin_image, destination_path)
        pbar.update(1)

    print(f"Image copiée : {chemin_image} -> {destination_path}")
    return True
