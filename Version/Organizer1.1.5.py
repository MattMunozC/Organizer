#GUI
import tkinter
from tkinter import filedialog
from tkinter import *
from tkinter import ttk

#visor
from PIL import ImageTk, Image


#mensajes
from tkinter import messagebox

#util
from shutil import move as shmove
from os import getcwd, listdir,remove
from os import rename as shrename
from os import mkdir as shmkdir

#keylistener
from pynput import keyboard

#TODO 
#--add a button to create new folders WIP
#--add keyboard listener WIP
#--add favorite label 
#--get file name option
#--format converter

#UPDATE
#1.1.4:
#--MenuBar Added
#--Image Info tab Added
#--undo stack bug fixed
#1.1.5:
#--New Folder button Added
#--MenuBar "Editar" name changed to "herramientas"
#--Language changed to English
WIDTH=1200
HEIGHT=780
SUPPORTED_TYPE=[".jpg",".png",".jpeg",".gif"]
try:
    with open("config.ini","r",encoding="UTF-8") as config:
        config={i.split("=")[0]:i.split("=")[1]for i in config.read().split("\n")}
except:
    config={}
class File():
    def __init__(self,filename):
        self.raw=filename.split(".")
        self.extension=f".{self.raw[-1]}"
        self.filename=".".join(self.raw[:-1])
        self.copy_num=0
    def __str__(self):
        return ".".join(self.raw) if self.copy_num==0 else f"{self.filename}({self.copy_num}){self.extension}"
    def rename(self):
        self.copy_num+=1
class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        
        self.listener = keyboard.Listener(on_press=self.on_press) 
        self.listener.start()
        self.num_button=0 #number of button added to the GUI
        self.current_row=0
        self.current_column=0
        self.current_path=getcwd()

        self.img=None

        botton_colors=[
            {
                "bg":"#ede2e1",
                "fg":"#000000"
            },
            {
                "bg":"#fa0000",
                "fg":"#ffffff"
            },
            {
                "bg":"#0000fa",
                "fg":"#ffffff"
            },
            {
                "bg":"#00ff00",
                "fg":"#ffffff"
            }
            ]

        self.path=ttk.Entry(width=70)
        self.path.place(x=20,y=10)

        self.file_list=[]
        self.move_img=[]
        self.undostack=[]

        self.current_img=0

#       fixed button
        self.vault_button=tkinter.Button(self,text="to vault", width=13,height=1,bg=botton_colors[3]["bg"],fg=botton_colors[3]["fg"],command=self.move_to_vault)
        self.vault_button.place(x=1000,y=745)

        self.directory_button=tkinter.Button(self,text="examinate",width=13,height=1,bg=botton_colors[0]["bg"],fg=botton_colors[0]["fg"],command=self.get_directory) #lack command parameter add later
        self.directory_button.place(x=450,y=8)

        self.next_button=tkinter.Button(self,text="next",width=13,height=1,bg=botton_colors[0]["bg"],fg=botton_colors[0]["fg"],command=self.next)
        self.next_button.place(x=400,y=745)

        self.previous_button=tkinter.Button(self,text="previous",width=13,height=1,bg=botton_colors[0]["bg"],fg=botton_colors[0]["fg"],command=self.previous)
        self.previous_button.place(x=250,y=745)

        self.undo_button=tkinter.Button(self,text="undo",width=13,height=1,bg=botton_colors[0]["bg"],fg=botton_colors[0]["fg"],command=self.Undo_Last_Action)
        self.undo_button.place(x=755, y=745)

        self.delete_button=tkinter.Button(self,text="delete", width=13,height=1,bg=botton_colors[1]["bg"],fg=botton_colors[1]["fg"],command=self.Delete_File)
        self.delete_button.place(x=20,y=745)

        self.yeet_button=tkinter.Button(self,text="Yeet", width=13,height=1,bg=botton_colors[2]["bg"],fg=botton_colors[2]["fg"],command=self.Move_File_Outside_Folder)
        self.yeet_button.place(x=600,y=745)

#       menubar
        menubar = Menu(self)
        self.config(menu=menubar)

        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Crop Image")
        editmenu.add_command(label="Search Image on Google")
        editmenu.add_command(label="convert Image")
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Image Info",command=self.info_tab)
        helpmenu.add_separator()
        helpmenu.add_command(label="About...")

        menubar.add_cascade(label="Tools", menu=editmenu)
        menubar.add_cascade(label="Help", menu=helpmenu)
###
        #self.testing()
###
#       Visor de imagenes
        self.viewer=tkinter.Frame(self,highlightbackground="black", highlightthickness=2,width=700,height=700)
        self.viewer.place(x=20,y=40)

        self.button_frame=tkinter.Frame(self,width=700,height=700)
        self.button_frame.place(x=750,y=40)
        
#       configuraciones de la GUI
        self.title("Organizer")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        #self.iconbitmap("Source/icon.ico")
        self.resizable(True,True)

        self.start_up()
    def info_tab(self):  
        messagebox.showinfo(message=f"Image Name: {self.file_list[self.current_img]}\n Path: {self.current_path}/{self.file_list[self.current_img]}",title="Image Information")
    def start_up(self):
        if bool(config):
            self.path.insert(0,config["last_visited_path"])
            self.load_folders(config["last_visited_path"])
    def Move_File_Outside_Folder(self):
        src=r"{path}/{img}".format(path=self.current_path,img=self.file_list[self.current_img])
        dst=r"{path}".format(path=self.current_path[:self.current_path.rfind("/")])
        try:
            shmove(src,dst)
        except:
            shrename(src,self.file_list[self.current_img])
        self.next()
    def Delete_File(self):
        remove(r"{path}/{img_name}".format(path=self.current_path,img_name=self.file_list[self.current_img]))
        self.next()
    def Undo_Last_Action(self):
        if len(self.undostack)==0:
            messagebox.showerror(message="No previous Move available",title="undo error")
        else:
            undo=self.undostack[-1]
            print(undo['path'])
            src=r"{path}/{name}".format(path=undo['path'],name=undo['img_name'])
            dst=r"{}".format(self.current_path)
            shmove(src,dst)
            self.move_img.remove(undo['img_name'])
            self.undostack.remove(undo)
            self.previous()
    def next(self):
        if len(self.move_img)==len(self.file_list):
                messagebox.showinfo(message="All Images sorted",title="task complete")
        else:
            while(1): 
                self.current_img=(self.current_img+1)%len(self.file_list)
                try:
                    self.load_img()
                    break
                except:
                    pass
    def previous(self):
        if len(self.move_img)==len(self.file_list):
                messagebox.showinfo(message="All Images sorted",title="task complete")

        else:
            while(1): 
                self.current_img=(self.current_img-1)%len(self.file_list)
                try:
                    self.load_img()
                    break
                except:
                    pass
    def move(self,pathname:str):
        file=File(self.file_list[self.current_img]) 
        while(1):
            try:
                src=r"{path}/{img}".format(path=self.current_path,img=str(file))
                dst=r"{path}/{newfolder}".format(path=self.current_path,newfolder=pathname)
                shmove(src,dst)
                break
            except:
                file.rename()
                newsrc=r"{path}/{img}".format(path=self.current_path,img=str(file))
                print(file)
                shrename(src,newsrc)
                src=newsrc
        self.move_img.append(self.file_list[self.current_img])
        self.undostack.append({"img_name":self.file_list[self.current_img],"path":dst})
        self.next()
    def get_directory(self):
        dir_path=filedialog.askdirectory(initialdir=self.current_path,title="Select Directory")
        self.path.delete(0, tkinter.END)
        self.path.insert(0,dir_path)
        self.load_folders(dir_path)
    def load_folders(self,dir_path):
        self.restart_frame()
        self.current_path=dir_path
        folder_list=[i for i in listdir(dir_path) if "." not in i]
        self.file_list=[i for i in listdir(dir_path) if "." in i and File(i).extension in SUPPORTED_TYPE] 
        self.file_list.sort()
        for i in folder_list:
            self.add_button(i)
        y_axis_value=(8+30*self.current_row)
        x_axis_value=10+200*self.current_column
        new_button=tkinter.Button(self.button_frame,text="Create Folder",bg="#00ff00",fg="#ffffff",width=26,height=1,command=lambda: self.show_new_folder_window())
        new_button.place(x=x_axis_value,y=y_axis_value)
        self.load_img()
    def load_img(self)->None:
        self.img=Image.open(f"{self.current_path}/{self.file_list[self.current_img]}")
        self.img.thumbnail((700,700))
        self.img=ImageTk.PhotoImage(self.img)
        img_viewer=tkinter.Label(self.viewer,image=self.img,anchor="center")
        img_viewer.place(relx=0.5, rely=0.5, anchor=CENTER)
    def add_button(self,name: str):
        margin=100
        y_axis_value=(8+30*self.current_row)
        x_axis_value=10+200*self.current_column
        if y_axis_value>self.button_frame.winfo_height()-margin:
            self.current_column+=1
            self.current_row=-1
        new_button=tkinter.Button(self.button_frame,text=name,width=26,height=1,command=lambda: self.move(name))
        new_button.place(x=x_axis_value,y=y_axis_value)
        self.num_button+=1
        self.current_row+=1
    def show_new_folder_window(self):
        self.new_folder= tkinter.Toplevel(self)
        self.new_folder.wm_title("Create a new folder")

        #entry
        entry_name=tkinter.Entry(self.new_folder,width=60)
        entry_name.place(x=10,y=40)

        #button
        create_folder_button=tkinter.Button(self.new_folder,text="Create Folder",bg="#00ff00",fg="#ffffff",width=26,height=1,command=lambda: self.create_new_folder(entry_name.get()))
        create_folder_button.place(x=10,y=150)

        cancel=tkinter.Button(self.new_folder,text="Cancel",bg="#ff0000",fg="#000000",width=26,height=1,command=lambda: print("canceled"))
        self.new_folder.geometry(f"400x200")
        self.new_folder.resizable(False,False)
    def create_new_folder(self,name):
        shmkdir(f"{self.current_path}/{name}")
        self.load_folders(self.current_path)
        messagebox.showinfo(message=f"Folder {name} created successfully")
        self.new_folder.destroy()
    def restart_frame(self):
        for item in self.button_frame.winfo_children(): item.destroy()
        for widget_image in self.viewer.winfo_children(): widget_image.destroy()
        self.restart_var()
    def restart_var(self):
        self.num_button=0
        self.current_row=0
        self.current_column=0
    def move_to_vault(self):
        src=r"{path}/{img}".format(path=self.current_path,img=self.file_list[self.current_img])
        dst=r"C:/Users/Soulx/Desktop/Baul"
        shmove(src,dst)
        self.move_img.append(self.file_list[self.current_img])
        self.undostack.append({"img_name":self.file_list[self.current_img],"path":dst})
        self.next()
    def on_press(self,key):
        try:
            if(key==key.left and self.file_list):
                self.previous()
            elif(key==key.right and self.file_list):
                self.next()
            elif(key==key.delete):
                self.Delete_File()
            elif(key==key.end):
                self.Move_File_Outside_Folder()
        except:
            pass

#######################TESTING AREA###################################################
    def testing(self):
        add_button=tkinter.Button(self,text="add",width=13,height=1,command=self.add_button_test)
        add_button.place(x=480,y=8)
        test=tkinter.Button(self,text="del",width=13,height=1,command=self.destroy_frame)
        test.place(x=520,y=8)
    def add_button_test(self):
        margin=100
        my_num=self.num_button
        y_axis_value=(8+30*self.current_row)
        x_axis_value=10+120*self.current_column
        if y_axis_value>self.button_frame.winfo_height()-margin:
            self.current_column+=1
            self.current_row=-1
        new_button=tkinter.Button(self.button_frame,text=f"button{self.num_button}",width=13,height=1,command=lambda: self.test(my_num))
        new_button.place(x=x_axis_value,y=y_axis_value)
        self.num_button+=1
        self.current_row+=1

    def test(self,param):
        print(f"{self.current_path}/{param}")
#######################TESTING AREA END###################################################        
if __name__=="__main__":
    window=App()
    #window.state('zoomed')
    window.mainloop()
