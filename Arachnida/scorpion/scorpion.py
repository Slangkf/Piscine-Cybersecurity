import argparse # to parse arguments
from PIL import Image # to open images
import exifread # to read EXIF metadata
import os

# Command line arguments parsing
parser = argparse.ArgumentParser(description='Display EXIF and other metadata from images.')
parser.add_argument('path', type=str, nargs='+', help='the path of the selected image(s)')

# Parses the command line arguments and stores them in the args variable.
args = parser.parse_args()

# Set of authorized image extensions to filter the images to be downloaded.
authorized_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp'}

# Checks if EXIF metadata is present in the image and displays it.
def display_exif_metadata(image_path):
    try:
        with open(image_path, 'rb') as image_file:
            tags = exifread.process_file(image_file)
            if tags:
                print(f"\nEXIF data found in the image {image_path}:")
                for tag, value in tags.items():
                    print(f"{tag}: {value}")
            else:
                print(f"\nNo EXIF data in the image {image_path}.")
    except Exception as e:
        print(f"\nException raised while reading EXIF data from {image_path}: {e}")

# Checks if the image can be opened and displays its format, mode, and size.
def display_image_metadata(image_path):
    try:
        with Image.open(image_path) as img:
            print(f"\n{image_path} image metadata:")
            print(f"Format: {img.format}")
            print(f"Mode: {img.mode}")
            print(f"Size: {img.size}")
    except Exception as e:
        print(f"\nException raised while reading image metadata from {image_path}: {e}")

# Iterates through the provided image paths, checks if they are authorized image formats, and displays their EXIF and other metadata.
for file in args.path:
    extension = os.path.splitext(file)[1].lower()
    if extension not in authorized_extensions:
        print(f"\nFile {file} is not an authorized image format. Skipping.")
        continue
    display_exif_metadata(file)
    display_image_metadata(file)