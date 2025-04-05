from tkinter import PhotoImage

import customtkinter as ctk
from os import path
from PIL import Image
from FileSorter.Utility import ToolTip as ttp

IMG_HEIGHT = 30
IMG_WIDTH = 30
MAX_LENGTH = 40

class Settings(ctk.CTkFrame):
    def __init__(self, controller, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)

        #header
        self.header = ctk.CTkFrame(self,corner_radius=5,fg_color="#1E1E1E")
        self.header.grid(row=0,column=0,padx=8,pady=(8, 4),sticky='nw')

        header_label = ctk.CTkLabel(self.header,text="Settings",font=("Bold", 30),corner_radius=0,width=75,justify="left",anchor="w")
        header_label.pack(side=ctk.LEFT,padx=(8,0),pady=(5,2))

        #body
        self.body = ctk.CTkFrame(self,corner_radius=5,fg_color="transparent")
        self.body.grid(row=1,column=0,sticky='nsew')
        self.body.columnconfigure(0,weight=0)
        self.body.columnconfigure(1,weight=3)
        self.body.columnconfigure(2,weight=0)
        self.body.columnconfigure(2,weight=0)

        #load images
        self.images_dir = path.join(path.dirname(path.realpath(__file__)),"icons")

        search_icon_name = "search_icon.png"
        search_path = path.join(self.images_dir, search_icon_name)
        search_image = ctk.CTkImage(Image.open(search_path),size=(IMG_WIDTH,IMG_HEIGHT))

        info_icon_name = "info_icon.png"
        info_path = path.join(self.images_dir,info_icon_name)
        info_image = ctk.CTkImage(Image.open(info_path),size=(IMG_WIDTH,IMG_HEIGHT))

        #display settings
        #file path
        self.filepath_label = ctk.CTkLabel(self.body,text="Files Location:",font=("Bold",20),
                                           corner_radius=0,justify="left",anchor="w")
        self.filepath_label.grid(row=0,column=0,padx=(8,0),pady=5,sticky="nw")

        self.filepath = search_path
        self.filepath_path_label = ctk.CTkLabel(self.body,text=self.filepath,anchor='w')
        self.filepath_path_label.grid(row=0,column=1,pady=5,sticky="new")
        if len(self.filepath) > MAX_LENGTH:
            self.filepath_ttp = ttp.CreateToolTip(self.filepath_path_label,self.filepath)

        self.filepath_search_btn = ctk.CTkButton(self.body, text="",hover=False,image=search_image,
                                                 bg_color="transparent",fg_color="transparent",
                                                 width=IMG_WIDTH,height=IMG_HEIGHT,
                                                 command=lambda: self.findPath())
        self.filepath_search_btn.grid(row=0,column=2,pady=(0,5))

        #target path
        self.targetpath_label = ctk.CTkLabel(self.body, text="Target Location: ",font=("Bold", 20),
                                             corner_radius=0,justify="left",anchor="w")
        self.targetpath_label.grid(row=1,column=0,padx=8,pady=5,sticky="nw")

        self.targetpath = "no path found!"
        self.targetpath_path_label = ctk.CTkLabel(self.body,text=self.targetpath,anchor='w')
        self.targetpath_path_label.grid(row=1,column=1,pady=5,sticky="new")
        if len(self.targetpath) > MAX_LENGTH:
            self.targetpath_ttp = ttp.CreateToolTip(self.targetpath_path_label,self.targetpath)

        self.targetpath_search_btn = ctk.CTkButton(self.body,text="",hover=False,image=search_image,
                                                   bg_color="transparent",fg_color="transparent",
                                                   width=IMG_WIDTH,height=IMG_HEIGHT,
                                                   command=lambda: self.findPath())
        self.targetpath_search_btn.grid(row=1,column=2,pady=(0,5))

    def findPath(self):
        print('the correct path often shows itself when you least expect it. -sun tzu probably')
