import pandas as pd
from pathlib import Path

# Chemin vers le fichier CSV
file_path = Path(r"/home/hiphen/Documents/GCP/data/my_data/filtered_data/data_filtered_jpg.csv")  

# Charger le fichier CSV
data = pd.read_csv(file_path, sep=';')

# Générer un dictionnaire pour les keypoints
keypoint_info = {}
for idx in range(len(data)):
    keypoint_info[idx] = {
        "name": f"keypoint_{idx}",
        "id": idx,
        "color": [255, 0, 0],  # Couleur 
        "type": "custom",  # Type générique
        "swap": ""  # Pas de point opposé défini ici
    }

# Générer un squelette de base 
skeleton_info = {}

# Créer le contenu du fichier de configuration avec une mise en page propre
dataset_info_content = f"dataset_info = dict(\n"
dataset_info_content += "    dataset_name='custom_dataset',\n"
dataset_info_content += "    paper_info=dict(\n"
dataset_info_content += "        author='Nom de l\'auteur',\n"
dataset_info_content += "        title='Titre du projet',\n"
dataset_info_content += "        container='Description',\n"
dataset_info_content += "        year='2025',\n"
dataset_info_content += "        homepage='URL ou description'\n"
dataset_info_content += "    ),\n"
dataset_info_content += "    keypoint_info={\n"

# Ajouter les keypoints avec une mise en page correcte
for idx, info in keypoint_info.items():
    dataset_info_content += f"        {idx}: {info},\n"

dataset_info_content = dataset_info_content.rstrip(",\n") + "\n    },\n"  # Enlever la dernière virgule
dataset_info_content += "    skeleton_info={},\n"
dataset_info_content += "    joint_weights=[1.0] * len(keypoint_info),\n"
dataset_info_content += "    sigmas=[0.025] * len(keypoint_info)\n"
dataset_info_content += ")"

# Chemin pour sauvegarder le fichier de configuration
output_path = Path(r"/home/hiphen/Documents/GCP/data/configs/meta_info.py")

# Créer le dossier s'il n'existe pas
output_path.parent.mkdir(parents=True, exist_ok=True)

# Écrire le fichier de configuration
with open(output_path, "w") as file:
    file.write(dataset_info_content)

print(f"Le fichier de configuration a été généré : {output_path.resolve()}")
