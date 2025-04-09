from dataset import BrainTumorDataset
from torch.utils.data import DataLoader

image_dir = "/Users/yashvi/Desktop/brats_final/filtered_images"
mask_dir = "/Users/yashvi/Desktop/brats_final/filtered_masks"

dataset = BrainTumorDataset(image_dir, mask_dir)
dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

for i, (images, masks) in enumerate(dataloader):
    print(f"Batch {i + 1}")
    print("Image shape:", images.shape)  # Should be [B, 1, 128, 128]
    print("Mask shape:", masks.shape)    # Should be [B, 1, 128, 128]
    break
