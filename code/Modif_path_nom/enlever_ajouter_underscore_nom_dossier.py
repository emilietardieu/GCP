import os
from pathlib import Path

def enlever_underscore(directory):
    "supprime underscore au debut et a la fin du nom d'un dossier"
    # Parcourir tous les dossiers dans le répertoire
    for folder in directory.iterdir():
        if folder.is_dir():  # Vérifie si c'est bien un dossier
            # Supprime les underscores au début du nom du dossier
            new_name = folder.name.lstrip("_").rstrip("_")
            new_folder_path = folder.parent / new_name  # Construit le nouveau chemin

            # Renomme le dossier si nécessaire
            if folder.name != new_name:
                folder.rename(new_folder_path)
                print(f"Dossier renommé : '{folder.name}' -> '{new_name}'")


def ajouter_underscore(directory):
    "ajoute underscore au debut du nom d'un dossier"
    # Parcourir tous les dossiers dans le répertoire
    for folder in directory.iterdir():
        if folder.is_dir():  # Vérifie si c'est bien un dossier
            # Ajoute un underscore au début du nom du dossier
            new_name = f"_{folder.name}"
            new_folder_path = folder.parent / new_name  # Construit le nouveau chemin

            # Renomme le dossier si nécessaire
            if folder.name != new_name:
                folder.rename(new_folder_path)
                print(f"Dossier renommé : '{folder.name}' -> '{new_name}'")



# Chemin du répertoire contenant les dossiers
directory = Path("/home/hiphen/Documents/GCP/data/my_data/images")

# ajouter_underscore(directory)
# enlever_underscore(directory)