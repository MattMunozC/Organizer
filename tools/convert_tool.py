from PIL import Image,ImageFile
from os import listdir
ImageFile.LOAD_TRUNCATED_IMAGES=True
PATH=f"C:\\Users\\Soulx\\Desktop\\Webp"
TARGET=f"C:\\Users\\Soulx\\Desktop\\Webp\\Converted"

DIRLIST=[file for file in listdir(PATH) if ".webp" in file]
for image in DIRLIST:
    Image.open(f"{PATH}\\{image}").convert("RGB").save(f"{TARGET}\\{image[:-5]}.png","png")
