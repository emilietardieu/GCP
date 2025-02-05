from model import UNet
import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader
from tqdm import tqdm
from GcpDataset import *
import wandb

LEARNING_RATE = 0.001
NUM_EPOCHS = 50
BATCH_SIZE = 4

def train(model, dataloader, criterion, optimizer, num_epochs, device):
    model.train()
    model.to(device)
    for epoch in range(num_epochs):
        running_loss = 0.0
        for inputs, targets in tqdm(dataloader):
            inputs, targets = inputs.to(device), targets.to(device)
            
            # Zero the parameter gradients
            optimizer.zero_grad()
            
            # Forward pass
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            
            # Backward pass and optimize
            loss.backward()
            optimizer.step()
            
            # Print statistics
            running_loss += loss.item()
        
        epoch_loss = running_loss / len(dataloader)
        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss}")
        
        # Log the loss to wandb
        wandb.log({ "loss": epoch_loss})

# Initialize wandb
wandb.init(project="unet-keypoint-detection", config={
    "learning_rate": LEARNING_RATE,
    "epochs": NUM_EPOCHS,
    "batch_size": BATCH_SIZE
})

# Create model
model = UNet()
wandb.watch(model)

# Create DataLoader
image_dir = 'images_256x256'  # Directory containing images
keypoints_file = 'gt.csv'  # CSV file containing keypoints
train_dataset = KeypointDataset(image_dir, keypoints_file, transform = transform )  # Initialize your dataset
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)

# Define loss function and optimizer
criterion = nn.MSELoss()
optimizer = optim.Adam(model.parameters(), lr= LEARNING_RATE )

# Check for GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

if __name__ == '__main__':
    # Train the model
    train(model, train_loader, criterion, optimizer, NUM_EPOCHS, device=device)