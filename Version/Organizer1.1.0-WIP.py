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

#TODO 
#--add a button to create new folders


WIDTH=1200
HEIGHT=780
UNSUPPORTED_TYPE=[".ini"]
class color():
    def rgb(R:int,G:int,B:int)->str:
        if R<255 and G<255 and B<255:
            print("hola")
        return f"#{hex(R)[-2:]}{hex(G)[-2:]}{hex(B)[-2:]}"

class App(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.num_button=0 #number of button added to the GUI
        self.current_row=0
        self.current_column=0
        self.current_path=""

        self.img=None

        botton_colors=[{"bg":"#ede2e1","fg":"#000000"},{"bg":"#fa0000","fg":"#ffffff"},{"bg":"#0000fa","fg":"#ffffff"}]

        self.path=ttk.Entry(width=70)
        self.path.place(x=20,y=10)

        self.file_list=[]
        self.move_img=[]
        self.undostack=[]

        self.current_img=0

#       fixed button
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
###
        #self.testing()
###
#       Visor de imagenes
        self.viewer=tkinter.Frame(self,highlightbackground="black", highlightthickness=2,width=700,height=700)
        self.viewer.place(x=20,y=40)

        self.button_frame=tkinter.Frame(self,width=450,height=700)
        self.button_frame.place(x=750,y=40)
        
#       configuraciones de la GUI
        self.title("Organizer")
        self.geometry(f"{WIDTH}x{HEIGHT}")
        #self.iconbitmap("Source/icon.ico")
        self.resizable(False, False)
    def Move_File_Outside_Folder(self):
        src=r"{path}/{img}".format(path=self.current_path,img=self.file_list[self.current_img])
        dst=r"{path}".format(path=self.current_path[:self.current_path.rfind("/")])
        shmove(src,dst)
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
        src=r"{path}/{img}".format(path=self.current_path,img=self.file_list[self.current_img])
        dst=r"{path}/{newfolder}".format(path=self.current_path,newfolder=pathname)
        shmove(src,dst)
        self.move_img.append(self.file_list[self.current_img])
        self.undostack.append({"img_name":self.file_list[self.current_img],"path":dst})
        self.next()

    def get_directory(self):
        self.restart_frame()
        dir_path=filedialog.askdirectory(initialdir=getcwd(),title="Select Directory")
        self.path.delete(0, tkinter.END)
        self.path.insert(0,dir_path)
        self.current_path=dir_path
        folder_list=[i for i in listdir(dir_path) if "." not in i]
        self.file_list=[i for i in listdir(dir_path) if "." in i and i[i.rfind("."):] not in UNSUPPORTED_TYPE] 
        self.file_list.sort()
        for i in folder_list:
            self.add_button(i)
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
    def restart_frame(self):
        for item in self.button_frame.winfo_children(): item.destroy()
        for widget_image in self.viewer.winfo_children(): widget_image.destroy()
        self.restart_var()
    def restart_var(self):
        self.num_button=0
        self.current_row=0
        self.current_column=0
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