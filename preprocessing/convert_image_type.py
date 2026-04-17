import os
import rasterio
import shutil

# Define raw path and create interim path
path = "./data/raw/raw_flood_map/"
interim_path = "./data/interim/flood_map_clean/"

if not os.path.exists(interim_path):
    os.makedirs(interim_path)

# Read all image files
all_images = os.listdir(path)

# Seperate different type of image files
image_tif = []
image_tiff = []
image_hdr = []

for i in all_images:
    if ".tiff" in i:
        image_tiff.append(i)
    elif ".tif" in i:
        image_tif.append(i)
    else:
        image_hdr.append(i)

# Create function to convert image from .tiff to .tif file
def convert_to_tif(input_path, output_path, image):
    with rasterio.open(input_path + image) as src:
        data = src.read()
        profile = src.profile
        profile.update(driver='GTiff')
    
    # Save images to the interim folder instead of the raw folder
    output_filename = image.replace(".tiff", ".tif")
    with rasterio.open(output_path + output_filename, 'w', **profile) as dst:
        dst.write(data)

# Delete the old files with .tiff and .hdr types
for image in image_tiff:
    convert_to_tif(path, interim_path, image)
    os.remove(path + image)

for image in image_tif:
    shutil.copy(path + image, interim_path + image)

# Test to verify the images in interim folders can be read successfully
test = os.listdir(interim_path)
for t in test:
    try:
        with rasterio.open(interim_path + t) as ds:
            # Read the first band
            data = ds.read(1) 
            print(f"--- Info for: {t} ---")
            print(f"Resolution (Res): {ds.res}")
            print(f"Shape (H, W): {ds.shape}")
            print("Status: Successfully opened and read.\n")
    
    except Exception as e:
        print(f"Error: Could not open {t}. Reason: {e}")