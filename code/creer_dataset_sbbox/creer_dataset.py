from annotation_images_cropped import *
from keypoint_dict import decouper_images_avec_keypoints
from pathlib import Path
from separation_train_val import separer_train_val

root = Path(r"/home/hiphen/Documents/GCP/data/my_data/Test_data/toutes_les_images_res4")
fichier_csv = Path(r"/home/hiphen/Documents/GCP/data/my_data/filtered_data/test_reel/tout_sauf_testcsv.csv") # le fichier doit contenir colonnes nouveau_path

csv_metadata = root/"sous_images_metadata.csv"
images_cropped = root/"images_cropped"
csv_gt = images_cropped/"gt.csv"

def creer_dataset(fichier_csv, csv_metadata, images_cropped, csv_gt ):
    root.mkdir(parents=True, exist_ok=True)

    chekpoints_path = root/"checkpoints"
    chekpoints_path.mkdir(parents=True, exist_ok=True)

    out_path = root/"out"
    out_path.mkdir(parents=True, exist_ok=True)

    test_path= root/"test"
    test_path.mkdir(parents=True, exist_ok=True)

    decouper_images_avec_keypoints(fichier_csv,images_cropped, csv_metadata, crop_size=512, prob_empty=0.01, resize_factor_avant=2, resize_factor_apres=2, overlap=0.3)
    create_gt_csv(csv_metadata, csv_gt)
    separer_train_val(images_cropped, csv_gt, root, train_size=0.8, random_state=42)


creer_dataset(fichier_csv, csv_metadata, images_cropped, csv_gt )




# images_test = root/"test"/"images"
images_test = Path(r"/home/hiphen/Documents/GCP/data/my_data/dataset_advanta/images_originales")
csv_metadata_test = root/"test"/"sous_images_metadata.csv"

def creer_test(fichier_csv, csv_metadata_test, images_test ):
    root.mkdir(parents=True, exist_ok=True)

    decouper_images_avec_keypoints(fichier_csv,images_test, csv_metadata_test, crop_size=1024, prob_empty=1, resize_factor_avant=2, resize_factor_apres=4, overlap=0.3)


# creer_test(fichier_csv, csv_metadata_test, images_test )