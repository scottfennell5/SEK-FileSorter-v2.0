import customtkinter as ctk
import os
from PIL import Image
from Utility import ToolTip as ttp

IMG_HEIGHT = 30
IMG_WIDTH = 30
MAX_LENGTH = 50

class Settings(ctk.CTkFrame):
    def __init__(self, controller, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)


        self.header = ctk.CTkFrame(self,corner_radius=5,fg_color="#1E1E1E")
        self.header.grid(row=0,column=0,pady=(8, 4),sticky='nw')
        self.populateHeader()

        self.body = ctk.CTkFrame(self,corner_radius=5,fg_color="transparent")
        self.body.grid(row=1,column=0,sticky='nsew')
        self.body.columnconfigure(0,weight=0)
        self.body.columnconfigure(1,weight=3)
        self.body.columnconfigure(2,weight=0)
        self.body.columnconfigure(2,weight=0)
        self.populateBody()

    def populateHeader(self):
        header_label = ctk.CTkLabel(self.header, text="Settings", font=("Bold", 30), corner_radius=0, width=75,
                                    justify="left", anchor="w")
        header_label.pack(side=ctk.LEFT, padx=(8, 0), pady=(5, 2))

    def populateBody(self):
        # load images
        search_path = self.controller.getResource("PersistentData\Icons\search_icon.png")
        print(f"search:{search_path}")
        search_image = ctk.CTkImage(Image.open(search_path), size=(IMG_WIDTH, IMG_HEIGHT))

        info_path = self.controller.getResource("PersistentData\Icons\info_icon.png")
        info_image = ctk.CTkImage(Image.open(info_path), size=(IMG_WIDTH, IMG_HEIGHT))

        # display settings
        # file path
        filepath_label = ctk.CTkLabel(self.body, text="Scanned Files:", font=("Bold", 20),
                                           corner_radius=0, justify="left", anchor="w")
        filepath_label.grid(row=0, column=0, padx=(8, 0), pady=5, sticky="nw")

        filepath = self.controller.getPath("files")
        filepath_path_label = ctk.CTkButton(self.body, text=filepath, anchor='w',
                                                 fg_color="transparent", bg_color="transparent", hover_color="#2b2b2b",
                                                 command=lambda: self.changeDirectory("files"))
        filepath_path_label.grid(row=0, column=1, pady=5, sticky="new")
        if len(filepath) > MAX_LENGTH:
            filepath_ttp = ttp.CreateToolTip(filepath_path_label, filepath)

        filepath_view_btn = ctk.CTkButton(self.body, text="", hover=False, image=search_image,
                                               bg_color="transparent", fg_color="transparent",
                                               width=IMG_WIDTH, height=IMG_HEIGHT,
                                               command=lambda: self.viewDirectory(filepath))
        filepath_view_btn.grid(row=0, column=2, pady=(0, 5))

        # target path
        targetpath_label = ctk.CTkLabel(self.body, text="Client Directory: ", font=("Bold", 20),
                                             corner_radius=0, justify="left", anchor="w")
        targetpath_label.grid(row=1, column=0, padx=8, pady=5, sticky="nw")

        targetpath = self.controller.getPath("target")
        targetpath_path_label = ctk.CTkButton(self.body, text=targetpath, anchor='w',
                                                   fg_color="transparent", bg_color="transparent",
                                                   hover_color="#2b2b2b",
                                                   command=lambda: self.changeDirectory("target"))
        targetpath_path_label.grid(row=1, column=1, pady=5, sticky="new")
        if len(targetpath) > MAX_LENGTH:
            targetpath_ttp = ttp.CreateToolTip(targetpath_path_label, targetpath)

        targetpath_search_btn = ctk.CTkButton(self.body, text="", hover=False, image=search_image,
                                                   bg_color="transparent", fg_color="transparent",
                                                   width=IMG_WIDTH, height=IMG_HEIGHT,
                                                   command=lambda: self.viewDirectory(targetpath))
        targetpath_search_btn.grid(row=1, column=2, pady=(0, 5))

    def viewDirectory(self, path):
        try:
            os.startfile(path)
        except:
            print(f"attempt to open path: {path} failed, invalid path")

    def changeDirectory(self, pathID):
        print(f"changing path directory type: {pathID}")
