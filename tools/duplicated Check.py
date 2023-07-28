from PIL import Image,ImageChops,ImageFile
from os import listdir
from time import sleep
import threading
ImageFile.LOAD_TRUNCATED_IMAGES = True
SUPPORTED_TYPE=[".jpg",".png",".jpeg",".gif",".JPG",".PNG",".JPEG",".GIF",".webp",".JPE"]

class File():
    def __init__(self,filename,path=""):
        self.raw=filename.split(".")
        self.extension=f".{self.raw[-1]}"
        self.filename=".".join(self.raw[:-1])
        self.copy_num=0
        self.path=path
    def __str__(self):
        return ".".join(self.raw) if self.copy_num==0 else f"{self.filename}({self.copy_num}){self.extension}"
    def rename(self):
        self.copy_num+=1
def equal(img1, img2):
    equal_size = img1.height == img2.height and img1.width == img2.width

    if img1.mode == img2.mode == "RGBA":
        img1_alphas = [pixel[3] for pixel in img1.getdata()]
        img2_alphas = [pixel[3] for pixel in img2.getdata()]
        equal_alphas = img1_alphas == img2_alphas
    else:
        equal_alphas = True

    equal_content = not ImageChops.difference(
        img1.convert("RGB"), img2.convert("RGB")
    ).getbbox()

    return equal_size and equal_alphas and equal_content

PATH="INSERT YOUR PATH HERE"

TARGET_PATH="INSERT YOUR PATH HERE"

PATH_LIST=[file for file in listdir(PATH) if File(file).extension in SUPPORTED_TYPE]
TARGET_LIST=[file for file in listdir(TARGET_PATH) if File(file).extension in SUPPORTED_TYPE]

output={}
def checker(list,leader=False):
    for image in list:
        image_PIL=Image.open(f"{PATH}\\{image}")
        for target_image in TARGET_LIST:
            try:
                target_image_PIL=Image.open(f"{TARGET_PATH}\\{target_image}")
                if equal(image_PIL,target_image_PIL):
                    output[image]=target_image
                    print(f"{image} is equal to {target_image}")
                    break
                else:
                    print(f"{image} is not equal to {target_image}")
            except:
                pass
    if (thread_num==0):
        print(output)
thread_num=6
cut=int(len(PATH_LIST)/6)

t1=threading.Thread(target=checker,args=(PATH_LIST[:cut:],True))
t2=threading.Thread(target=checker,args=(PATH_LIST[cut::]))
t1.start()
t2.start()

"""
This whole bit works but it's slowe as all hell, please do not even try to run it unless you want to freeze your own computer, the general purpose of this little project was to 
compare a list of images to another, it was made and tested with a sample of 5000 images and it's as simple as it gets, perhaps i'll come back to this someday, wiser and older
but for now, this is just a flop project. 

"""
