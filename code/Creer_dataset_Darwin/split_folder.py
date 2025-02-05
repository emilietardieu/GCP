from pathlib import Path
import shutil

def split_folder(input_folder, output_base, subfolders_per_split):
    input_folder = Path(input_folder)
    output_base = Path(output_base)

    # Vérification de l'existence du dossier d'entrée
    if not input_folder.is_dir():
        raise ValueError(f"Le dossier spécifié n'existe pas : {input_folder}")

    # Récupération des sous-dossiers
    subfolders = [f for f in input_folder.iterdir() if f.is_dir()]

    # Initialisation des variables
    split_index = 1
    current_split_folder = output_base / f"split{split_index}"
    current_split_folder.mkdir(parents=True, exist_ok=True)

    # Parcours des sous-dossiers par groupe de 'subfolders_per_split'
    for i, subfolder in enumerate(subfolders):
        if i > 0 and i % subfolders_per_split == 0:
            # Passer au prochain split
            split_index += 1
            current_split_folder = output_base / f"split{split_index}"
            current_split_folder.mkdir(parents=True, exist_ok=True)

        # Copier le sous-dossier dans le split actuel
        shutil.copytree(subfolder, current_split_folder / subfolder.name, dirs_exist_ok=True)

    print(f"Dossiers divisés en {split_index} parties dans {output_base}")

# Exemple d'utilisation
split_folder(
    input_folder="/home/hiphen/Documents/GCP/data/my_data/darwin_json",
    output_base="/home/hiphen/Documents/GCP/data/my_data/split_data",
    subfolders_per_split=10
)
