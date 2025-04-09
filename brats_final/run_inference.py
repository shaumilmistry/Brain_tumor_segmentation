import os
import torch
import numpy as np
from PIL import Image
from test_dataset import TumorDataset
from unet_model import UNet
from torch.utils.data import DataLoader
import torchvision.transforms as transforms

# Load device (GPU if available)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Paths
image_dir = 'converted_images'
mask_dir = 'converted_masks'
output_dir = 'predicted_masks'

# Create output folder if not exists
os.makedirs(output_dir, exist_ok=True)

# Image transformations
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor()
])

# Dataset & DataLoader
dataset = TumorDataset(image_dir, mask_dir, transform=transform)
loader = DataLoader(dataset, batch_size=1, shuffle=False)

# Load Model
model = UNet()
model.load_state_dict(torch.load('unet_model.pth', map_location=device))
model.to(device)
model.eval()

# Inference loop
with torch.no_grad():
    for i, (image, _) in enumerate(loader):
        image = image.to(device)
        output = model(image)
        output = torch.sigmoid(output)
        output = output.squeeze().cpu().numpy()

        # Convert to binary mask
        binary_mask = (output > 0.5).astype(np.uint8) * 255

        # Save the mask
        Image.fromarray(binary_mask).save(os.path.join(output_dir, f"pred_{i:03d}.png"))

print("✅ Tumor segmentation completed and saved to 'predicted_masks' folder.")
