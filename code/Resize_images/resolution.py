from PIL import Image
from pathlib import Path

def ajuster_resolution(n , dossier_entree , dossier_sortie):

    # Dossiers d'entrée et de sortie
    dossier_sortie.mkdir(exist_ok=True)  # Crée le dossier s'il n'existe pas

    # Parcourir toutes les images du dossier d'entrée
    for fichier in dossier_entree.glob("*.JPG"):  # Change "*.jpg" selon le format (ex: "*.png")
        image = Image.open(fichier)
        # print(image.width, image.height, fichier.name)
        nouvelle_taille = (image.width // n, image.height // n)  # Divise la résolution par 2
        image_resized = image.resize(nouvelle_taille)  # Suppression de Image.ANTIALIAS
        print(nouvelle_taille, fichier.name)
        return image_resized

        # Sauvegarde dans le dossier de sortie avec le même nom
        # image_resized.save(dossier_sortie / fichier.name)

    print("Toutes les images ont été réduites et enregistrées dans", dossier_sortie)
    return dossier_sortie

    # dossier_entree = Path("/home/hiphen/Documents/GCP/data/my_data/Resize_data/resolution/images_originales_resolution")
    # dossier_sortie = Path("/home/hiphen/Documents/GCP/data/my_data/Resize_data/resolution/images_test_resolution")