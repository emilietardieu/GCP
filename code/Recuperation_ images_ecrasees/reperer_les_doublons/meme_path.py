import pandas as pd

# Charger le fichier CSV
fichier_csv= "/home/hiphen/Documents/GCP/data/my_data/filtered_data/advanta_csv.csv"
output_file = "/home/hiphen/Documents/GCP/data/my_data/filtered_data/doublons_advanta.csv"
df = pd.read_csv(fichier_csv, sep=";")  # Remplacer read_excel par read_csv pour un fichier CSV

# Spécifie la colonne contenant les chemins
colonne_chemins = "path"  # Vérifie le nom exact de la colonne dans le fichier CSV


# Vérifie si la colonne existe
if colonne_chemins not in df.columns:
    print(f"La colonne '{colonne_chemins}' n'existe pas dans le fichier.")
else:
    # Trouver les doublons dans la colonne 'path'
    doublons = df[df.duplicated(subset=[colonne_chemins], keep=False)]

    # Afficher les lignes contenant des doublons
    print(f"Les lignes avec des doublons :\n{doublons[colonne_chemins]}")
    doublons.to_csv(output_file, index=False)