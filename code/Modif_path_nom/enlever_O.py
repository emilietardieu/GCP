import os
from pathlib import Path

# Chemin du dossier parent contenant les dossiers à renommer
parent_directory = Path("/home/hiphen/Documents/GCP/data/my_data/darwin_json")

# Parcours des sous-dossiers
for folder in parent_directory.iterdir():
    if folder.is_dir():  # Vérifie si c'est bien un dossier
        new_name = folder.name.replace("O:_", "")  # Remplace "O:" par rien
        new_folder_path = parent_directory / new_name
        
        # Renomme le dossier
        if new_name != folder.name:  # Évite de renommer si aucun changement
            folder.rename(new_folder_path)
            print(f"Dossier renommé : '{folder.name}' -> '{new_name}'")

