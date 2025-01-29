from pathlib import Path
import shutil
import os

def rename_images_by_path(directory):
    directory = Path(directory)
    if not directory.is_dir():
        raise ValueError(f"{directory} n'est pas un dossier valide.")
    
    for image in directory.rglob("*.*"):
        if image.is_file():
            # Crée un nouveau nom basé sur le chemin relatif
            relative_path = image.relative_to(directory).parent.as_posix()
            sanitized_name = relative_path.replace("/", "_").replace("AV", "").replace("RGB", "").replace("dataset", "").replace("image_undistort", "").rstrip("_")
            new_name = f"{directory.name}_{sanitized_name}_{image.name}"
            new_path = image.parent / new_name  # Le fichier reste dans le même dossier

            try:
                image.rename(new_path)
                print(f"Renommé : {image.name} -> {new_name}")
            except Exception as e:
                print(f"Erreur en renommant {image.name} : {e}")


def move_images_to_root_and_cleanup(folder_path):
    root_folder = Path(folder_path)

    # Vérifie que le dossier racine existe
    if not root_folder.is_dir():
        print(f"Erreur : Le dossier {folder_path} n'existe pas ou n'est pas valide.")
        return

    print(f"Début du traitement pour le dossier : {folder_path}")

    # Parcourt les sous-dossiers en profondeur (de bas en haut pour suppression des sous-dossiers)
    for subdir, dirs, files in os.walk(folder_path, topdown=False):
        subdir_path = Path(subdir)
        for file in files:
            file_path = subdir_path / file  # Chemin complet du fichier
            dest_file = root_folder / file  # Destination dans le dossier racine

            # Si un fichier du même nom existe, ajouter un suffixe
            counter = 1
            while dest_file.exists():
                dest_file = root_folder / f"{file_path.stem}_{counter}{file_path.suffix}"
                counter += 1

            try:
                shutil.move(str(file_path), str(dest_file))  # Déplace le fichier
                print(f"Fichier déplacé : {file_path} -> {dest_file}")
            except Exception as e:
                print(f"Erreur lors du déplacement de {file_path} : {e}")

        # Vérifie si le sous-dossier est vide et le supprime
        if subdir_path != root_folder and not any(subdir_path.iterdir()):
            try:
                subdir_path.rmdir()
                print(f"Sous-dossier supprimé : {subdir_path}")
            except Exception as e:
                print(f"Erreur lors de la suppression du sous-dossier {subdir_path} : {e}")

    print("Opération terminée : toutes les images ont été déplacées et les sous-dossiers vides supprimés.")



# Exemple d'utilisation
directory = "/home/hiphen/Documents/GCP/data/my_data/sbbox/images_test/autres_test"


#rename_images_by_path(directory)
move_images_to_root_and_cleanup(directory)
