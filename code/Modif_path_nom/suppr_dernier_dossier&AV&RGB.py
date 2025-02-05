# Supoprime le dernier dossier et les dossier "AV" et "RGB"

from pathlib import Path
import shutil
from tqdm import tqdm

def move_images_and_cleanup(root_folder):
    # Convertir le chemin en objet Path
    root = Path(root_folder)

    # Vérifier si le chemin est un dossier
    if not root.is_dir():
        print("Le chemin spécifié n'est pas un dossier valide.")
        return

    # Parcourir tous les fichiers dans les sous-dossiers
    for file_path in root.rglob("*.*"):  # Trouver tous les fichiers avec une extension
        if file_path.is_file():  # Vérifier si c'est un fichier
            parent_dir = file_path.parent  # Récupérer le dossier parent
            grandparent_dir = parent_dir.parent  # Récupérer l'avant-dernier dossier

            if grandparent_dir.exists():  # Vérifier que l'avant-dernier dossier existe
                new_path = grandparent_dir / file_path.name  # Construire le nouveau chemin
                file_path.rename(new_path)  # Déplacer le fichier
                print(f"Déplacé : {file_path} -> {new_path}")

    # Supprimer les dossiers vides
    for dir_path in sorted(root.rglob("*"), reverse=True):  # Parcourir les dossiers en ordre inverse
        if dir_path.is_dir() and not any(dir_path.iterdir()):  # Vérifier si le dossier est vide
            dir_path.rmdir()  # Supprimer le dossier
            print(f"Dossier supprimé : {dir_path}")


def enlever_dossiers_av_rgb(root_folder):
    # Convertir le chemin en objet Path
    root = Path(root_folder)

    # Vérifier si le chemin est un dossier
    if not root.is_dir():
        print("Le chemin spécifié n'est pas un dossier valide.")
        return

    # Parcourir tous les sous-dossiers
    for folder in tqdm(root.rglob("*")):  # Parcourt récursivement tous les dossiers
        if folder.is_dir() and folder.name in ["AV", "RGB"]:  # Vérifie si le dossier est 'AV' ou 'RGB'
            parent_dir = folder.parent  # Récupère le dossier parent

            # Déplacer tout le contenu du dossier AV ou RGB dans le parent
            for item in folder.iterdir():
                target_path = parent_dir / item.name
                if target_path.exists():
                    print(f"Le fichier {target_path} existe déjà, il sera ignoré.")
                else:
                    shutil.move(str(item), target_path)  # Déplace chaque fichier ou dossier

            # Supprimer le dossier AV ou RGB vide
            folder.rmdir()
            print(f"Dossier supprimé : {folder}")


# Chemin du dossier racine
root_folder = "/home/hiphen/Documents/GCP/data/my_data/darwin_json"
move_images_and_cleanup(root_folder)
enlever_dossiers_av_rgb(root_folder)




