from regroupement_dossier import *
from annotation_images_cropped import *
from keypoint_dict import *


fichier_csv = "/home/hiphen/Documents/GCP/data/my_data/filtered_data/advanta_bayer.csv"
output_dir = "/home/hiphen/Documents/GCP/data/my_data/Resize_data/advanta_bayer/images"
csv_output = "/home/hiphen/Documents/GCP/data/my_data/Resize_data/advanta_bayer/sous_images_metadata.csv"


def creer_dataset():

    regroupement_dosssier(fichier_csv, dossier_images)
                             
    decouper_images_avec_keypoints(fichier_csv, dossier_images, csv_output)
                  