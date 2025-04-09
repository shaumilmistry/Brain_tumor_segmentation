import os
import shutil

# Corrected Paths
base_path = os.path.expanduser("~/Desktop/brats_final")
image_folder = os.path.join(base_path, "converted_image")   # fixed this
mask_folder = os.path.join(base_path, "converted_masks")

# New folders to save filtered images & masks
final_images = os.path.join(base_path, "final_images")
final_masks = os.path.join(base_path, "final_masks")

# Create new folders if they don't exist
os.makedirs(final_images, exist_ok=True)
os.makedirs(final_masks, exist_ok=True)

# Choose a slice number
slice_number = 20

# Loop through image files
for image_file in os.listdir(image_folder):
    if image_file.endswith(".png"):
        base_name = image_file.replace(".png", "")
        mask_file = f"{base_name}_slice_{slice_number}.png"

        image_path = os.path.join(image_folder, image_file)
        mask_path = os.path.join(mask_folder, mask_file)

        if os.path.exists(mask_path):
            shutil.copy(image_path, os.path.join(final_images, image_file))
            shutil.copy(mask_path, os.path.join(final_masks, image_file))  # rename mask to match image
        else:
            print(f"❌ Mask not found for: {image_file}")

print("✅ DONE! Check the 'final_images' and 'final_masks' folders inside brats_final.")
