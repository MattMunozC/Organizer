from sys import argv
from os import listdir
from PIL import Image
from shutil import move
from pprint import pprint
SUPPORTED_TYPE=[".jpg",".png",".jpeg",".gif",".JPG",".PNG",".JPEG",".GIF",".webp",".JPE"]
PATH=argv[1]

class File():
    def __init__(self,filename,path=""):
        self.CORRUPT_PATH=f"{path}\\Rotten"
        self.GOOD_PATH=f"{path}\\GoodState"
        self.raw=filename.split(".")
        self.extension=f".{self.raw[-1]}"
        self.filename=".".join(self.raw[:-1])
        self.copy_num=0
        self.path=path
    def __str__(self):
        return ".".join(self.raw) if self.copy_num==0 else f"{self.filename}({self.copy_num}){self.extension}"
    def rename(self):
        self.copy_num+=1
    #If Image from PIL can't open it, chances are that the file is damaged, this a easy way and quick way to check although is not exact and can get false positive
    def integrity_check(self):
        try:
            Image.open(f"{self.path}\\{self.filename}{self.extension}")
            return True
        except: 
            return False
    def move(self,state="Good"):
        state_dict={"Good":self.GOOD_PATH,"Bad":self.CORRUPT_PATH}
        move(f"{self.path}\\{str(self)}",f"{state_dict[state]}\\{str(self)}")
DIR_LIST=[image for image in listdir(PATH) if File(image).extension in SUPPORTED_TYPE]
