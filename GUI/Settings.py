from tkinter import filedialog
import customtkinter as ctk
import os
from PIL import Image
from Utility import ToolTip as ttp
from CTkMessagebox import CTkMessagebox
import logging

IMG_HEIGHT = 30
IMG_WIDTH = 30
MAX_LENGTH = 50

FILES_ID = "files"
TARGET_ID = "target"

NO_PATH = "no path found!"

class Settings(ctk.CTkFrame):
    def __init__(self, controller, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.filepath = self.controller.get_path(FILES_ID)
        self.targetpath = self.controller.get_path(TARGET_ID)
        self.pending_changes = False
        self.grid_columnconfigure(0,weight=1)


        self.header = ctk.CTkFrame(self,corner_radius=5,fg_color="#1E1E1E")
        self.header.grid(row=0,column=0,padx=5,pady=5,sticky='nw')
        self.populate_header()

        self.body = ctk.CTkFrame(self,corner_radius=5,fg_color="transparent")
        self.body.grid(row=1,column=0,padx=5,pady=5,sticky='nsew')
        self.body.columnconfigure(0,weight=0)
        self.body.columnconfigure(1,weight=1)
        self.body.columnconfigure(2,weight=0)
        self.populate_body()

        self.footer = ctk.CTkFrame(self,corner_radius=5,fg_color="transparent")
        self.footer.grid(row=2,column=0,sticky='nsew')

    def populate_header(self):
        header_label = ctk.CTkLabel(self.header, text="Settings", font=("Bold", 30), corner_radius=0, width=75,
                                    justify="left", anchor="w")
        header_label.pack(side=ctk.LEFT, padx=(8, 0), pady=(5, 2))

    def populate_body(self):
        # load images
        search_path = self.controller.get_resource("PersistentData\Icons\search_icon.png")
        print(f"search:{search_path}")
        search_image = ctk.CTkImage(Image.open(search_path), size=(IMG_WIDTH, IMG_HEIGHT))

        # display settings
        # file path
        filepath_label = ctk.CTkLabel(self.body, text="Scanned Files:", font=("Bold", 20),
                                           corner_radius=0, justify="left", anchor="w")
        filepath_label.grid(row=0, column=0, padx=(8, 0), pady=5, sticky="nw")

        if self.filepath == "":
            text = NO_PATH
        else:
            text = self.filepath
        filepath_path_label = ctk.CTkButton(self.body, text=text, anchor='w',
                                            fg_color="transparent", bg_color="transparent", hover_color="#2b2b2b",
                                            command=lambda: self.change_directory(FILES_ID))
        filepath_path_label.grid(row=0, column=1, pady=5, sticky="new")
        if len(self.filepath) > MAX_LENGTH:
            ttp.CreateToolTip(filepath_path_label, self.filepath)

        filepath_view_btn = ctk.CTkButton(self.body, text="", hover=False, image=search_image,
                                          bg_color="transparent", fg_color="transparent",
                                          width=IMG_WIDTH, height=IMG_HEIGHT,
                                          command=lambda: self.view_directory(self.filepath))
        filepath_view_btn.grid(row=0, column=2, pady=(0, 5))

        # target path
        targetpath_label = ctk.CTkLabel(self.body, text="Client Directory: ", font=("Bold", 20),
                                             corner_radius=0, justify="left", anchor="w")
        targetpath_label.grid(row=1, column=0, padx=8, pady=5, sticky="nw")

        if self.targetpath == "":
            text = NO_PATH
        else:
            text = self.targetpath
        targetpath_path_label = ctk.CTkButton(self.body, text=text, anchor='w',
                                              fg_color="transparent", bg_color="transparent",
                                              hover_color="#2b2b2b",
                                              command=lambda: self.change_directory(TARGET_ID))
        targetpath_path_label.grid(row=1, column=1, pady=5, sticky="new")
        if len(self.targetpath) > MAX_LENGTH:
            ttp.CreateToolTip(targetpath_path_label, self.targetpath)

        targetpath_search_btn = ctk.CTkButton(self.body, text="", hover=False, image=search_image,
                                              bg_color="transparent", fg_color="transparent",
                                              width=IMG_WIDTH, height=IMG_HEIGHT,
                                              command=lambda: self.view_directory(self.targetpath))
        targetpath_search_btn.grid(row=1, column=2, pady=(0, 5))

    def populate_footer(self):
        apply_button = ctk.CTkButton(self.footer, text="Apply", width=125,
                                     fg_color="#CBC3E3", text_color="black", hover_color="#2E2E2E",
                                     command=lambda: self.apply_changes())
        apply_button.pack(side=ctk.RIGHT, padx=4, pady=5)

        cancel_button = ctk.CTkButton(self.footer, text="Cancel", width=125,
                                      fg_color="#1E1E1E", text_color="#BB86FC", hover_color="#2E2E2E",
                                      command=lambda: self.cancel_changes())
        cancel_button.pack(side=ctk.RIGHT, padx=4, pady=5)

    def clear_footer(self):
        for widget in self.footer.winfo_children():
            widget.destroy()

    def update(self):
        for widget in self.body.winfo_children():
            widget.destroy()

        self.populate_body()

        if self.pending_changes:
            self.populate_footer()
        else:
            self.clear_footer()

    def view_directory(self, path):
        try:
            os.startfile(path)
        except OSError:
            print(f"attempt to open path: {path} failed, invalid path")

    def change_directory(self, pathID):
        path = filedialog.askdirectory(initialdir=self.controller.get_base_directory(),
                                       title=f"Please select the directory you would like to change {pathID} to.")

        if path == "":
            logging.debug("path is empty, no action taken")
            return

        if pathID == FILES_ID:
            if self.targetpath == path:
                CTkMessagebox(title="Error", icon="warning",
                              message="Error: Scanned Files directory cannot be the same as Client directory! \nPlease choose a new path.")
            else:
                self.filepath = path
        elif pathID == TARGET_ID:
            if self.filepath == path:
                CTkMessagebox(title="Error", icon="warning",
                              message="Error: Client directory cannot be the same as Scanned Files directory! \nPlease choose a new path.")
            else:
                self.targetpath = path
        self.pending_changes = True
        self.update()

    def apply_changes(self):
        if self.filepath != "":
            self.controller.set_path(FILES_ID, self.filepath)
        if self.targetpath != "":
            self.controller.set_path(TARGET_ID, self.targetpath)

        self.controller.save_settings()
        self.pending_changes = False
        self.update()

    def cancel_changes(self):
        self.filepath = self.controller.get_path(FILES_ID)
        self.targetpath = self.controller.get_path(TARGET_ID)
        self.pending_changes = False
        self.update()