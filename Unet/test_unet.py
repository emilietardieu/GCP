from model import UNet
import torch
from torch.utils.data import DataLoader
from GcpDataset import *
import matplotlib.pyplot as plt

# Load the model
model = UNet()
model.load_state_dict(torch.load('model.pth'))  # Load the trained model weights
model.eval()

# Check for GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Create DataLoader
image_dir = 'images_256x256'  # Directory containing images
keypoints_file = 'gt.csv'  # CSV file containing keypoints
test_dataset = KeypointDataset(image_dir, keypoints_file, transform=transform)  # Initialize your dataset
test_loader = DataLoader(test_dataset, batch_size=1, shuffle=False)

# Test the model
def test(model, dataloader, device):
    model.eval()
    with torch.no_grad():
        for inputs, targets in dataloader:
            inputs, targets = inputs.to(device), targets.to(device)
            
            # Forward pass
            outputs = model(inputs)
            
            # Print the results
            print(f"Predicted: {outputs.cpu().numpy()}, Actual: {targets.cpu().numpy()}")
            
            # Visualize the results
            img = inputs.cpu().squeeze().permute(1, 2, 0).numpy()
            plt.imshow(img)
            plt.scatter(outputs.cpu().numpy()[0][0], outputs.cpu().numpy()[0][1], c='r', marker='x')
            plt.scatter(targets.cpu().numpy()[0][0], targets.cpu().numpy()[0][1], c='g', marker='o')
            plt.show()

if __name__ == '__main__':
    test(model, test_loader, device)
