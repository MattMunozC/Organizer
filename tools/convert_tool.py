from PIL import Image,ImageFile
from os import listdir
ImageFile.LOAD_TRUNCATED_IMAGES=True
PATH={"PATH"}
TARGET={"TARGET"}

DIRLIST=[file for file in listdir(PATH) if ".webp" in file]
for image in DIRLIST:
    Image.open(f"{PATH}\\{image}").convert("RGB").save(f"{TARGET}\\{image[:-5]}.png","png")
