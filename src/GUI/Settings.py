from tkinter import filedialog

import customtkinter as ctk
import os
from PIL import Image
from CTkMessagebox import CTkMessagebox
import logging

from Core.Controller import Controller
import Utility.ToolTip as ttp
from Utility.constants import FILES_ID, TARGET_ID
from Utility.style import style_button_prominent, style_button, style_label_body_header, style_label_header, \
    style_path_button, style_invisible_frame

IMG_HEIGHT = 30
IMG_WIDTH = 30
MAX_LENGTH = 60
NO_PATH = "no path found! click here to select a path."

class Settings(ctk.CTkFrame):
    def __init__(self, controller:Controller, master:ctk.CTkFrame, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.file_path = self.controller.get_path(FILES_ID)
        self.target_path = self.controller.get_path(TARGET_ID)
        self.pending_changes = False
        self.grid_columnconfigure(0,weight=1)


        self.header = ctk.CTkFrame(self,**style_invisible_frame)
        self.header.grid(row=0,column=0,padx=5,pady=5,sticky='nw')
        self.populate_header()

        self.body = ctk.CTkFrame(self,**style_invisible_frame)
        self.body.grid(row=1,column=0,padx=5,pady=5,sticky='nsew')
        self.body.columnconfigure(0,weight=0)
        self.body.columnconfigure(1,weight=1)
        self.body.columnconfigure(2,weight=0)
        self.populate_body()

        self.footer = ctk.CTkFrame(self,**style_invisible_frame)
        self.footer.grid(row=2,column=0,sticky='nsew')

    def populate_header(self) -> None:
        for widget in self.header.winfo_children():
            widget.destroy()
        header_label = ctk.CTkLabel(self.header, text="Settings", **style_label_header)
        header_label.pack(side=ctk.LEFT, padx=(8, 0), pady=(5, 2))

    def populate_body(self) -> None:
        for widget in self.body.winfo_children():
            widget.destroy()

        def create_path_setting(row, label_text, path, path_id):
            label = ctk.CTkLabel(self.body, text=label_text, **style_label_body_header)
            label.grid(row=row, column=0, padx=(8, 0), pady=5, sticky="nw")

            display_text = NO_PATH if path == "" else path
            path_button = ctk.CTkButton(self.body, text=display_text, **style_path_button,
                                        command=lambda: self.change_directory(path_id))
            path_button.grid(row=row, column=1, pady=5, sticky="new")

            if len(path) > MAX_LENGTH:
                ttp.CreateToolTip(path_button, path)

        create_path_setting(
            row=0,
            label_text="Scanned Files:",
            path=self.file_path,
            path_id=FILES_ID
        )

        create_path_setting(
            row=1,
            label_text="Client Directory:",
            path=self.target_path,
            path_id=TARGET_ID
        )

    def populate_footer(self) -> None:
        for widget in self.footer.winfo_children():
            widget.destroy()

        apply_button = ctk.CTkButton(self.footer, text="Apply", **style_button_prominent, width=125,
                                     command=lambda: self.apply_changes())
        apply_button.pack(side=ctk.RIGHT, padx=4, pady=5)

        cancel_button = ctk.CTkButton(self.footer, text="Cancel", **style_button, width=125,
                                      command=lambda: self.cancel_changes())
        cancel_button.pack(side=ctk.RIGHT, padx=4, pady=5)

    def clear_footer(self) -> None:
        for widget in self.footer.winfo_children():
            widget.destroy()

    def update(self) -> None:
        for widget in self.body.winfo_children():
            widget.destroy()

        self.populate_body()

        if self.pending_changes:
            self.populate_footer()
        else:
            self.clear_footer()

    def view_directory(self, path:str) -> None:
        try:
            os.startfile(path)
        except OSError:
            logging.debug(f"attempt to open path: {path} failed, invalid path")

    def change_directory(self, pathID:str) -> None:
        path = filedialog.askdirectory(initialdir="C:\\",
                                       title=f"Please select the directory you would like to change {pathID} to.")

        if path == "":
            logging.debug("path is empty, no action taken")
            return

        if pathID == FILES_ID:
            if self.target_path == path:
                CTkMessagebox(title="Error", icon="warning",
                              message="Error: Scanned Files directory cannot be the same as Client directory! \nPlease choose a new path.")
            else:
                self.file_path = path
        elif pathID == TARGET_ID:
            if self.file_path == path:
                CTkMessagebox(title="Error", icon="warning",
                              message="Error: Client directory cannot be the same as Scanned Files directory! \nPlease choose a new path.")
            else:
                self.target_path = path
        self.pending_changes = True
        self.update()

    def apply_changes(self) -> None:
        if self.file_path != "":
            logging.debug(f"setting files_path to {self.file_path}")
            self.controller.set_path(FILES_ID, self.file_path)
        if self.target_path != "":
            logging.debug(f"setting target_path to {self.target_path}")
            self.controller.set_path(TARGET_ID, self.target_path)\

        self.controller.save_settings()
        self.pending_changes = False
        self.update()

    def cancel_changes(self) -> None:
        self.file_path = self.controller.get_path(FILES_ID)
        self.target_path = self.controller.get_path(TARGET_ID)
        self.pending_changes = False
        self.update()