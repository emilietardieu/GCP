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

# Afficher les points clés sur l'image
def display_keypoints(image_path, keypoints):
    image = cv2.imread(str(image_path))
    for point in keypoints:
        cv2.drawMarker(image, (int(point[0]), int(point[1])), (0, 255, 0), markerType=cv2.MARKER_CROSS, thickness=1)
    
    # Convertir l'image de BGR à RGB pour l'affichage avec matplotlib
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image_rgb)
    plt.axis('off')
    plt.show()

# Chemin vers le fichier CSV
csv_path = Path(r'/home/hiphen/Documents/GCP/data/my_data/Resize_data/advanta/sans_0/images_256x256/images_cropped_sans0_256x256/gt.csv')

# Charger les points clés
keypoints_data = load_keypoints(csv_path)

# Afficher les points clés sur les 10 premières images
for i in range(10):
    row = keypoints_data.iloc[i]
    image_path = Path(f"/home/hiphen/Documents/GCP/data/my_data/Resize_data/advanta/sans_0/images_256x256/images_cropped_sans0_256x256/{row['filename']}")
    display_keypoints(image_path, row['locations'])
