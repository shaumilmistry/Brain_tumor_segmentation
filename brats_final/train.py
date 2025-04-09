import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import transforms
from tqdm import tqdm

from unet import UNet
from test_dataset import BrainTumorDataset

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Paths to your image and mask folders
image_dir = "converted_image"
mask_dir = "converted_masks"

# Hyperparameters
lr = 1e-4
batch_size = 4
num_epochs = 20

# Transformations
transform = transforms.Compose([
    transforms.ToTensor(),
])

# Dataset and DataLoader
dataset = BrainTumorDataset(image_dir=image_dir, mask_dir=mask_dir, transform=transform)
loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

# Model, Loss, Optimizer
model = UNet(in_channels=1, out_channels=1).to(device)
loss_fn = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=lr)

# Training loop
for epoch in range(num_epochs):
    model.train()
    epoch_loss = 0
    loop = tqdm(loader)

    for data, targets in loop:
        data = data.to(device=device, dtype=torch.float)
        targets = targets.to(device=device, dtype=torch.float)

        # Forward
        predictions = model(data)
        loss = loss_fn(predictions, targets)

        # Backward
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        epoch_loss += loss.item()
        loop.set_description(f"Epoch [{epoch+1}/{num_epochs}]")
        loop.set_postfix(loss=loss.item())

    print(f"Epoch {epoch+1}/{num_epochs} | Loss: {epoch_loss / len(loader):.4f}")

# Save model
torch.save(model.state_dict(), "unet_brain_tumor.pth")
print("✅ Model trained and saved as unet_brain_tumor.pth")
