import os
import cv2
import numpy as np
from tqdm import tqdm
import shutil

# Step 1: Define the folder paths
base_path = "/Users/yashvi/Desktop/brats_final"
image_path = os.path.join(base_path, "converted_image")
mask_path = os.path.join(base_path, "converted_masks")

# Step 2: Create new folders to store only useful tumor slices
filtered_img_dir = os.path.join(base_path, "filtered_images")
filtered_mask_dir = os.path.join(base_path, "filtered_masks")
os.makedirs(filtered_img_dir, exist_ok=True)
os.makedirs(filtered_mask_dir, exist_ok=True)

# Step 3: Loop through all mask files
for mask_file in tqdm(os.listdir(mask_path)):
    mask_file_path = os.path.join(mask_path, mask_file)

    # Read the mask in grayscale
    mask = cv2.imread(mask_file_path, cv2.IMREAD_GRAYSCALE)
    if mask is None:
        continue

    # Step 4: Check if tumor exists (any white pixels)
    if np.any(mask > 0):
        # Extract the image name (like BRATS_001.png)
        image_id = "_".join(mask_file.split("_")[:2])  # e.g., BRATS_001
        img_file = f"{image_id}.png"
        img_file_path = os.path.join(image_path, img_file)

        # Step 5: Copy image + mask to new folder if image exists
        if os.path.exists(img_file_path):
            shutil.copy(img_file_path, os.path.join(filtered_img_dir, img_file))
            shutil.copy(mask_file_path, os.path.join(filtered_mask_dir, mask_file))
