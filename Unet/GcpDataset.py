import torch
from torch.utils.data import Dataset
from PIL import Image
import pandas as pd
import ast
import numpy as np
from torchvision import transforms

class KeypointDataset(Dataset):
    def __init__(self, image_dir, keypoints_file, transform=None):
        self.image_dir = image_dir
        self.data_frame = pd.read_csv(keypoints_file)
        self.transform = transform 


    def __len__(self):
        return len(self.data_frame)

    def __getitem__(self, idx):
        img_name = self.data_frame.iloc[idx, 0]
        img_path = f"{self.image_dir}/{img_name}"
        image = Image.open(img_path).convert('RGB')
        keypoints = ast.literal_eval(self.data_frame.iloc[idx, 2])
        keypoints = np.array(keypoints).flatten()
        keypoints = torch.tensor(keypoints, dtype=torch.float32)

        if self.transform:
            image = self.transform(image)

        return image, keypoints

# Definition transforms
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5], std=[0.5])
])

