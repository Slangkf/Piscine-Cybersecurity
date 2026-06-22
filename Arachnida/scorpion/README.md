*This project was created in June 2026 as part of the 42 curriculum by tclouet.*

![](../shared/note.png)

![](../shared/feedbacks.png)

# Description

*This section presents the project, its goals, and a brief overview.*

The Scorpion exercise aims to create a program that receives image files as command-line arguments and extracts EXIF and other metadata from them, displaying the information on the screen. 

The program is written in Python, and its dependencies are managed through a virtual environment created with venv.

# Instructions

*This section contains information about installation and execution.*

*Before starting, please ensure that Python 3.13 or later is installed.*

1. ### **Set up the virtual environment:**

    From the `scorpion` directory, run the following commands:
	
    - Create a virtual environment: `python -m venv venv`. 
    - Activate the virtual environment: `source venv/bin/activate`.
    - Install the required dependencies: `pip install Pillow exifread`.
    - Verify that the virtual environment is activated: `which python`.

#### Note:
    The `which python` command should return: `venv/bin/python`.

2. ### **Run the program:**

    - To display EXIF and other metadata from one or more image files: `python3 scorpion.py <image_path1> <image_path2> ...`

#### Note:
    To display the program help message, type: `python3 scorpion.py --help`

3. ### **Deactivate the virtual environment:**

    - To leave the virtual environment, run: `deactivate`.

# Technical Notes

*This section provides technical information about the technologies used in the project.*

### **Python dependencies:**

- Pillow: Image manipulation and processing.
- ExifRead: Extraction of EXIF ​​data from image files.

### **What is EXIF?**

EXIF (Exchangeable Image File Format) data contains technical information about the conditions under which an image was captured:

- Camera settings: Shutter speed, aperture, ISO.
- Date and time: Exact moment the image was taken.
- GPS coordinates: Location of the capture site.
- Software: Program used to edit the image (if applicable).

This information is usually embedded in the image metadata by digital cameras or smartphones, although it may be modified or removed by image-editing software or during export.
