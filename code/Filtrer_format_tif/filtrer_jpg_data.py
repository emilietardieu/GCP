import pandas as pd

# Charger le fichier CSV avec le bon séparateur
file_path = r'C:\Users\EmilieTardieu\Documents\GCP\data\my_markers_nas_2024-07-05.csv'  # Remplacez par le chemin de votre fichier
output_path = r'C:\Users\EmilieTardieu\Documents\GCP\data\my_data\filtered_data\data_filtered_jpg.csv'  # Chemin pour le fichier filtré

# Lire le fichier avec le bon séparateur
data = pd.read_csv(file_path, sep=';')

# Filtrer uniquement les lignes contenant des images en .JPG dans la colonne "camera"
jpg_data = data[data['camera'].str.endswith('.JPG', na=False)]

# Enregistrer les données filtrées dans un nouveau fichier CSV
jpg_data.to_csv(output_path, index=False)

print(f"Les données filtrées ont été enregistrées dans : {output_path}")
