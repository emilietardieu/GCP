import cv2
import pandas as pd
from pathlib import Path
from tqdm import tqdm

root = Path(r"/home/hiphen/Documents/GCP/data/my_data/dataset_advanta")
input_folder = root / "images_originales"
output_folder = root / "test"

def crop_images(root, input_folder, output_folder, resize_factor_avant=2, crop_size=1024, resize_factor_apres=4, overlap=0.4):
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)
    
    if not output_folder.exists():
        output_folder.mkdir(parents=True)
    
    metadata = []
    image_files = [f for f in input_folder.iterdir() if f.suffix.lower() in ['.png', '.jpg', '.jpeg']]
    
    for filename in tqdm(image_files, desc="Processing images"):
        img = cv2.imread(str(filename))
        file_name = filename.stem
        
        # Réduction de la résolution avant le cropping
        h, w, _ = img.shape
        img = cv2.resize(img, (int(w / resize_factor_avant), int(h / resize_factor_avant)))
        h, w, _ = img.shape
        
        crop_count = 0
        step = int(crop_size * (1 - overlap))
        for y_start in range(0, h - crop_size + 1, step):
            for x_start in range(0, w - crop_size + 1, step):
                x_end = x_start + crop_size
                y_end = y_start + crop_size
                
                crop = img[y_start:y_end, x_start:x_end]
                
                # Réduction de la résolution après le cropping
                crop = cv2.resize(crop, (int(crop_size / resize_factor_apres), int(crop_size / resize_factor_apres)))
                
                crop_filename = f"{file_name}_crop_{crop_count:04d}.JPG"
                crop_path = output_folder / crop_filename
                cv2.imwrite(str(crop_path), crop)
                
                # Save metadata
                metadata.append({
                    'crop_filename': crop_filename,
                    'x_start': x_start,
                    'y_start': y_start,
                    'x_end': x_end,
                    'y_end': y_end
                })

                crop_count += 1
        print(f"{crop_count} sous-images générées pour {filename.name}")
    
    # Save metadata to CSV
    metadata_df = pd.DataFrame(metadata)
    metadata_df.to_csv(root / 'metadata.csv', index=False)

# Example usage
crop_images(root, input_folder, output_folder)
