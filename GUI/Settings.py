from tkinter import filedialog
import customtkinter as ctk
import os
from PIL import Image
from CTkMessagebox import CTkMessagebox
import logging

from Utility import ToolTip as ttp
from Utility.constants import FILES_ID, TARGET_ID, BROWSER_ID

IMG_HEIGHT = 30
IMG_WIDTH = 30
MAX_LENGTH = 50
NO_PATH = "no path found! click here to select a path."

class Settings(ctk.CTkFrame):
    def __init__(self, controller, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.file_path = self.controller.get_path(FILES_ID)
        self.target_path = self.controller.get_path(TARGET_ID)
        self.browser_path = self.controller.get_path(BROWSER_ID)
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
        for widget in self.header.winfo_children():
            widget.destroy()
        header_label = ctk.CTkLabel(self.header, text="Settings", font=("Bold", 30), corner_radius=0, width=75,
                                    justify="left", anchor="w")
        header_label.pack(side=ctk.LEFT, padx=(8, 0), pady=(5, 2))

    def populate_body(self):
        for widget in self.body.winfo_children():
            widget.destroy()

        def create_path_setting(row, label_text, path, path_id, image, view_command=None):
            label = ctk.CTkLabel(self.body, text=label_text, font=("Bold", 20),
                                 corner_radius=0, justify="left", anchor="w")
            label.grid(row=row, column=0, padx=(8, 0), pady=5, sticky="nw")

            display_text = NO_PATH if path == "" else path
            path_button = ctk.CTkButton(self.body, text=display_text, anchor='w',
                                        fg_color="transparent", bg_color="transparent", hover_color="#2b2b2b",
                                        command=lambda: self.change_directory(path_id))
            path_button.grid(row=row, column=1, pady=5, sticky="new")

            if len(path) > MAX_LENGTH:
                ttp.CreateToolTip(path_button, path)

            if view_command and path != "":
                view_button = ctk.CTkButton(self.body, text="", hover=False, image=image,
                                         bg_color="transparent", fg_color="transparent",
                                         width=IMG_WIDTH, height=IMG_HEIGHT,
                                         command=view_command)
                view_button.grid(row=row, column=2, pady=(0, 5))

        search_path = self.controller.get_resource("PersistentData\Icons\search_icon.png")
        search_image = ctk.CTkImage(Image.open(search_path), size=(IMG_WIDTH, IMG_HEIGHT))

        create_path_setting(
            row=0,
            label_text="Scanned Files:",
            path=self.file_path,
            path_id=FILES_ID,
            image=search_image,
            view_command=lambda: self.view_directory(self.file_path)
        )

        create_path_setting(
            row=1,
            label_text="Client Directory:",
            path=self.target_path,
            path_id=TARGET_ID,
            image=search_image,
            view_command=lambda: self.view_directory(self.target_path)
        )

        create_path_setting(
            row=2,
            label_text="Browser:",
            path=self.browser_path,
            path_id=BROWSER_ID,
            image=None
        )

    def populate_footer(self):
        for widget in self.footer.winfo_children():
            widget.destroy()

        apply_button = ctk.CTkButton(self.footer, text="Apply", width=125,
                                     fg_color="#C3B1E1", text_color="black", hover_color="#CCCCFF",
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
        if pathID == BROWSER_ID:
            path = filedialog.askopenfilename(title="Select the EXE file for your browser",filetypes=[("Executables","*.exe")])
        else:
            path = filedialog.askdirectory(initialdir=self.controller.get_base_directory(),
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
        elif pathID == BROWSER_ID:
            self.browser_path = path
        self.pending_changes = True
        self.update()

    def select_browser(self):
        pass

    def apply_changes(self):
        if self.file_path != "":
            logging.debug(f"setting files_path to {self.file_path}")
            self.controller.set_path(FILES_ID, self.file_path)
        if self.target_path != "":
            logging.debug(f"setting target_path to {self.target_path}")
            self.controller.set_path(TARGET_ID, self.target_path)
        if self.browser_path != "":
            logging.debug(f"setting browser_path to {self.browser_path}")
            self.controller.set_path(BROWSER_ID, self.browser_path)

        self.controller.save_settings()
        self.pending_changes = False
        self.update()

    def cancel_changes(self):
        self.file_path = self.controller.get_path(FILES_ID)
        self.target_path = self.controller.get_path(TARGET_ID)
        self.browser_path = self.controller.get_path(BROWSER_ID)
        self.pending_changes = False
        self.update()