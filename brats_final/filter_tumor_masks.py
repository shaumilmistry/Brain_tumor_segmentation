import os
import shutil
import numpy as np
from PIL import Image

# Paths
base_path = os.path.expanduser("~/Desktop/brats_final")
image_folder = os.path.join(base_path, "converted_image")
mask_folder = os.path.join(base_path, "converted_masks")

# Output folders
final_images = os.path.join(base_path, "final_images")
final_masks = os.path.join(base_path, "final_masks")
os.makedirs(final_images, exist_ok=True)
os.makedirs(final_masks, exist_ok=True)

# Loop through each image like BRATS_001.png
for image_file in os.listdir(image_folder):
    if image_file.endswith(".png"):
        base_name = image_file.replace(".png", "")  # BRATS_001
        found_tumor = False

        # Loop through slices 0 to 39
        for i in range(40):
            mask_name = f"{base_name}_slice_{i}.png"
            mask_path = os.path.join(mask_folder, mask_name)

            if os.path.exists(mask_path):
                mask = Image.open(mask_path).convert("L")
                mask_array = np.array(mask)

                if np.any(mask_array > 0):
                    # Tumor found in this slice
                    found_tumor = True

                    # Copy image and corresponding mask
                    shutil.copy(os.path.join(image_folder, image_file), os.path.join(final_images, image_file))
                    shutil.copy(mask_path, os.path.join(final_masks, image_file))  # Rename to image name
                    break  # No need to check more slices for this image

        if not found_tumor:
            print(f"⚠️ No tumor found in any slice of {base_name}")

print("✅ Tumor-present masks and images copied successfully.")
