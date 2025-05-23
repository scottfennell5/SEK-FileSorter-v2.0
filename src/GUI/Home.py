import customtkinter as ctk
from functools import partial
import logging
import time

from Core.Controller import Controller
from GUI.FileInput import FileInput
from GUI.Table import Table
from Utility.constants import FILE_NAME, STATUS, CLIENT_NAME, RowData, DEFAULT_VALUES, FILE_PATH
from Utility.style import style_button, style_label_header, style_status_complete, style_status_incomplete, \
    style_sub_frame, style_label_body, style_invisible_frame


class Home(ctk.CTkFrame):
    def __init__(self, master:ctk.CTkBaseClass, controller:Controller, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.controller.set_observer(self)
        self.clients = None
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.header = ctk.CTkFrame(self,**style_invisible_frame)
        self.populate_header()
        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid(row=0,column=0,padx=5,pady=5,sticky='w')

        self.body = ctk.CTkFrame(self, **style_invisible_frame)
        self.body.columnconfigure(0,weight=1)
        self.table = Table(self.body, self.controller, **style_invisible_frame)
        self.populate_body()
        self.body.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

    def populate_header(self) -> None:
        col = 0
        header_label = ctk.CTkLabel(self.header, text="Home",**style_label_header)
        header_label.pack(side=ctk.LEFT,padx=(8,150),pady=(5,2))
        col += 1

        button_frame = ctk.CTkFrame(self.header, **style_invisible_frame)
        button_frame.pack(side=ctk.RIGHT, fill="x",expand=True, padx=8, pady=(5,2))

        sort_button = ctk.CTkButton(button_frame, text="Sort", **style_button, width=125,
                                    command=lambda: self.sort())
        sort_button.pack(side=ctk.RIGHT, padx=4)
        col += 1

        refresh_button = ctk.CTkButton(button_frame, text="Refresh Data", **style_button, width=125,
                                       command=lambda : self.update())
        refresh_button.pack(side=ctk.RIGHT,padx=4)
        col += 1

    def populate_body(self) -> None:
        start = time.time()

        files = self.controller.get_data_copy()
        logging.debug(f"populating table with {len(files)} files")
        if files.empty or files is None:
            label = ctk.CTkLabel(self.body,
                                 text="No files detected! \n\n\nIf you expected files here, \nmake sure the Scanned Files path in 'Settings' is correct.",
                                 justify="center",anchor="center")
            label.grid(row=0, column=0, padx=8, pady=5, sticky='new')
            return

        # grabs the specified columns below, and
        clients = list(zip(files[FILE_NAME], files[FILE_PATH], files[STATUS], files[CLIENT_NAME]))

        self.table.refresh_values(clients)
        self.table.place(relx=0, rely=0, relwidth=1, relheight=1)

        end = time.time()
        logging.debug(f"populate_table:{round(end - start, 3)}s")

    def open_file(self, file_data:RowData) -> None:
        inputOverlay = FileInput(self.controller, file_data, self, **style_sub_frame)

        start_y = 1.2
        target_y = 0.0
        steps = 20
        delay = 10

        def animate(step=0) -> None:
            progress = step / steps
            eased_progress = 1 - (1 - progress) ** 2

            current_y = start_y - (start_y - target_y) * eased_progress
            inputOverlay.place(relx=0, rely=current_y, relwidth=1, relheight=1)
            inputOverlay.lift()

            if step < steps:
                self.after(delay, animate, step + 1)
            else:
                inputOverlay.place(relx=0, rely=target_y, relwidth=1, relheight=1)

        animate()

    def close(self,widget:ctk.CTkBaseClass) -> None:
        start_y = 0.0
        target_y = 1.2
        steps = 20
        delay = 10

        def animate(step=0) -> None:
            progress = step / steps
            eased_progress = progress ** 2

            current_y = start_y + (target_y - start_y) * eased_progress
            widget.place_configure(rely=current_y)

            if step < steps:
                self.after(delay, animate, step + 1)
            else:
                widget.place_forget()
                self.after(500, widget.destroy)
                self.update()

        animate()

    def update(self) -> None:
        logging.debug("Refreshing the UI with updated data.")
        self.populate_body()

    def sort(self) -> None:
        self.controller.sort_files()