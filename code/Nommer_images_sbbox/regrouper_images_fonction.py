from pathlib import Path
from trouver_dans_archives import trouver_chemin_dans_archives
import shutil

def regrouper_dossiers_images(chemin_image , dossier_cible, fichier_csv):
    """
    Regroupe un dossier contenant des images JPEG dans un répertoire cible.
    Si plusieurs dossiers ont le même nom, utilise le chemin complet pour les différencier.

    Args:
        chemin_image  (str): Chemin du dossier source contenant l'arborescence initiale.
        dossier_cible (str): Chemin du dossier cible où regrouper les dossiers.
        chemins_archives (list): Liste des emplacements des archives.
    """
    chemin_image  = Path(chemin_image )
    dossier_cible = Path(dossier_cible)

    # Rechercher dans les archives si le chemin de l'image n'existe pas
    if not chemin_image.exists():
        print(f"\nChemin introuvable : {chemin_image }")
        chemin_image  = trouver_chemin_dans_archives(chemin_image )
        if not chemin_image :
            return False

    if chemin_image.exists():

        # Créer un nom basé sur le chemin parent de l'image
        nom_image = chemin_image.as_posix().replace("/", "_").replace("_media_nas-production_", "").replace("_media_nas-archives_", "").replace("_RGB", "").replace("_dataset", "").replace("_AV", "").replace("_image_undistort", "").replace(".JPG", "")
        chemin_destination = dossier_cible / f"{nom_image}{chemin_image.suffix}"

        # Copier avec barre de progression
        print(f"Copie de : {chemin_image}")
        #shutil.copy2(chemin_image, chemin_destination)
        print(f"Image copiée sous : {chemin_destination}")




        # # Obtenir le chemin relatif en ignorant les 3 premiers dossiers et en sautant le dernier
        # chemin_relatif = Path(*chemin_image.parts[3:-1])  # Ignorer "dataset"
        # chemin_destination = dossier_cible / chemin_relatif

        # # Créer les dossiers nécessaires
        # chemin_destination.mkdir(parents=True, exist_ok=True)

        # # Copier le fichier directement dans le dossier parent
        # print(f"Copie de : {chemin_image}")
        # shutil.copy2(chemin_image, chemin_destination / chemin_image.name)
        # print(f"Image copiée dans : {chemin_destination / chemin_image.name}")