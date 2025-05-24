from tkinter import filedialog
import customtkinter as ctk
import os
from CTkMessagebox import CTkMessagebox
import logging
import uuid

from Core.Controller import Controller
import Utility.ToolTip as ttp
from Utility.constants import FILES_ID, TARGET_ID
from Utility.style import style_button_prominent, style_button, style_label_body_header, style_label_header, \
    style_path_button, style_invisible_frame

MAX_LENGTH = 60
NO_PATH = "no path found! click here to select a path."

MD_ID = "id"
MD_ROW = "row"
MD_FRAME = "frame"
MD_LABEL = "label"
MD_PATH_BTN = "path_button"
MD_DEL_BTN = "delete_button"

class Settings(ctk.CTkFrame):
    def __init__(self, controller:Controller, master:ctk.CTkFrame, **kwargs):
        super().__init__(master, **kwargs)
        """
        self.controller = controller
        self.file_paths = self.controller.get_path(FILES_ID)
        self.target_path = self.controller.get_path(TARGET_ID)
        self.file_path_rows = []
        self.target_path_row = None
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
        self.populate_footer()
        self.footer.grid(row=2,column=0,sticky='nsew')

    def populate_header(self) -> None:
        for widget in self.header.winfo_children():
            widget.destroy()
        header_label = ctk.CTkLabel(self.header, text="Settings", **style_label_header)
        header_label.pack(side=ctk.LEFT, padx=(8, 0), pady=(5, 2))

    def populate_body(self) -> None:
        for widget in self.body.winfo_children():
            widget.destroy()

        target_row = self.create_path_row(
            row=0,
            label_text="Target Directory:",
            path=self.target_path,
            path_id=TARGET_ID,
            delete=False
        )
        self.target_path_row = target_row

        self.file_path_rows = []
        if self.file_paths:
            for i, file_path in enumerate(self.file_paths):
                row = self.create_path_row(
                    row=i+1,
                    path=self.file_paths[i],
                    path_id=FILES_ID
                )
                self.file_path_rows.append(row)

    def create_path_row(self, row:int, path_id:str, label_text:str= "", path:str= "", delete:bool=True) -> dict:
        unique_id = str(uuid.uuid4())
        frame = ctk.CTkFrame(**style_invisible_frame)

        if label_text:
            text = label_text
        else:
            text = f"File Directory {row+1}"
        label = ctk.CTkLabel(frame, text=text, **style_label_body_header)
        label.grid(row=row, column=0, padx=(8, 0), pady=5, sticky="nw")

        display_text = path if path else NO_PATH
        path_button = ctk.CTkButton(frame, text=display_text, **style_path_button,
                                    command=lambda: self.change_directory(path_id))
        path_button.grid(row=row, column=1, pady=5, sticky="new")

        if len(path) > MAX_LENGTH:
            ttp.CreateToolTip(path_button, path)

        if delete:
            delete_button = ctk.CTkButton(frame, text="Delete", **style_path_button,
                                          command=lambda: self.delete_path_row(unique_id))
            delete_button.grid(row=row, column=2, pady=5, sticky="new")
        else:
            delete_button = None

        metadata = {
            MD_ID:unique_id,
            MD_ROW: row,
            MD_FRAME: frame,
            MD_LABEL: label,
            MD_PATH_BTN: path_button,
            MD_DEL_BTN: delete_button
        }
        return metadata

    def delete_path_row(self, unique_id:str, confirmed:bool=False) -> None:
            for existing_row in self.file_path_rows:
                if existing_row[MD_ID] == unique_id:
                    path = existing_row[MD_PATH_STR]
                    self.file_paths.remove(path)
                    self.pending_changes=True
                    self.update()
        else:
            for existing_row in self.file_path_rows:
                if existing_row[MD_ID] == unique_id:
                    existing_row[MD_DEL_BTN].configure(text="Confirm Deletion",
                                                       command=self.delete_path_row(unique_id,
                                                                                    confirmed=True))


    def populate_footer(self) -> None:
        add_button = ctk.CTkButton(self.footer, text="Add File Directory", **style_button,
                                   command=lambda: self.create_path_row(row=len(self.file_path_rows)+1,
                                                                        path_id=FILES_ID))
        add_button.pack(side=ctk.LEFT, padx=4, pady=5)
        apply_button = ctk.CTkButton(self.footer, text="Apply", **style_button_prominent, width=125,
                                     command=lambda: self.apply_changes())

        cancel_button = ctk.CTkButton(self.footer, text="Cancel", **style_button, width=125,
                                      command=lambda: self.cancel_changes())

    def show_footer(self) -> None:
        for widget in self.footer.winfo_children():
            widget.pack(side=ctk.RIGHT, padx=4, pady=5)

    def clear_footer(self) -> None:
        for widget in self.footer.winfo_children():
            widget.pack_forget()

    def update(self) -> None:
        for widget in self.body.winfo_children():
            widget.destroy()

        self.populate_body()

        if self.pending_changes:
            self.show_footer()
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
        if self.target_path != "":
            logging.debug(f"setting target_path to {self.target_path}")
            self.controller.set_path(TARGET_ID, self.target_path)

        #TODO: for files in file paths, add to list and update list

        self.controller.save_settings()
        self.pending_changes = False
        self.update()

    def cancel_changes(self) -> None:
        self.file_path = self.controller.get_path(FILES_ID)
        self.target_path = self.controller.get_path(TARGET_ID)
        self.pending_changes = False
        self.update()
    """