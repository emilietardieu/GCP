import cv2
import pandas as pd
import matplotlib.pyplot as plt
import ast
from pathlib import Path

# Charger les points clés depuis le fichier CSV
def load_keypoints(csv_path):
    data = pd.read_csv(csv_path)
    data['locations'] = data['locations'].apply(ast.literal_eval)
    return data

# Afficher les points clés avec des cercles autour
def display_keypoints(image_path, keypoints, radius):
    image = cv2.imread(str(image_path))
    
    for point in keypoints:
        x, y = int(point[0]), int(point[1])
        
        # Dessiner un marqueur (croix)
        # cv2.drawMarker(image, (y, x), (0, 255, 0), markerType=cv2.MARKER_CROSS, thickness=1)
        
        # Dessiner un cercle autour du keypoint
        cv2.circle(image, (y, x), radius, (255, 0, 0), thickness=1)  # Bleu avec une épaisseur de 1 pixel

        cv2.circle(image, (y, x), 14, (255, 255, 0), thickness=1) 

    # Convertir l'image de BGR à RGB pour l'affichage avec matplotlib
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image_rgb)
    plt.axis('off')
    plt.show()

# Chemin vers le fichier CSV
csv_path = Path(r'/home/hiphen/Documents/GCP/data/my_data/Test_data/toutes_les_images/validation/images/gt.csv')

# Charger les points clés
keypoints_data = load_keypoints(csv_path)

# Afficher les points clés sur les 30 premières images avec des cercles de rayon r = 5
for i in range(2000,3000, 10):
    row = keypoints_data.iloc[i]
    image_path = Path(f"/home/hiphen/Documents/GCP/data/my_data/Test_data/toutes_les_images/validation/images/{row['filename']}")
    display_keypoints(image_path, row['locations'], radius=6)
