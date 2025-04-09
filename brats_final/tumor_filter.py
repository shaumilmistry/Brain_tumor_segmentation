import os
import shutil
import numpy as np
from PIL import Image

# Correct paths
base_path = os.path.expanduser("~/Desktop/brats_final")
image_folder = os.path.join(base_path, "converted_image")
mask_folder = os.path.join(base_path, "converted_masks")

# Output folders
final_images = os.path.join(base_path, "final_images")
final_masks = os.path.join(base_path, "final_masks")
os.makedirs(final_images, exist_ok=True)
os.makedirs(final_masks, exist_ok=True)

# Choose which slice number to check (same for all images)
slice_number = 20

# Loop through each image and check if corresponding mask has tumor
for image_file in os.listdir(image_folder):
    if image_file.endswith(".png"):
        base_name = image_file.replace(".png", "")
        mask_file = f"{base_name}_slice_{slice_number}.png"
        mask_path = os.path.join(mask_folder, mask_file)

        if os.path.exists(mask_path):
            mask = Image.open(mask_path).convert("L")  # grayscale
            mask_array = np.array(mask)

            if np.any(mask_array > 0):  # Check if tumor pixels are present
                # Copy image and mask
                shutil.copy(os.path.join(image_folder, image_file), os.path.join(final_images, image_file))
                shutil.copy(mask_path, os.path.join(final_masks, image_file))  # rename to match image
            else:
                print(f"🟡 No tumor in: {mask_file}")
        else:
            print(f"🔴 Mask missing for: {image_file}")

print("✅ Done! Only tumor-present masks & images copied.")
