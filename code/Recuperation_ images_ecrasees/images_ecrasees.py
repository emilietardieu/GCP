from pathlib import Path
import pandas as pd

# Recharger le fichier pour un traitement approprié
file_path = Path(r'C:\Users\EmilieTardieu\Documents\GCP\data\my_data\filtered_data\data_filtered_jpg.csv')
data = pd.read_csv(file_path, delimiter=';')

# Identifier les noms de caméra qui se répètent
repeated_cameras = data['camera'][data['camera'].duplicated(keep=False)]

# Obtenir les noms uniques et leur fréquence
repeated_camera_counts = repeated_cameras.value_counts()

# Afficher les résultats
print("Noms de caméra répétés et leur fréquence :")
print(repeated_camera_counts)
