import customtkinter as ctk
from functools import partial
import logging
import time

from Core.Controller import Controller
from GUI.FileInput import FileInput
from Utility.constants import FILE_NAME, STATUS, CLIENT_NAME, FileData, DEFAULT_VALUES
from Utility.style import style_button, style_label_header, style_status_complete, style_status_incomplete, \
    style_sub_frame, style_label_body, style_invisible_frame


class Home(ctk.CTkFrame):
    def __init__(self, controller:Controller, master:ctk.CTkBaseClass, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.clients = None
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.header = ctk.CTkFrame(self,**style_invisible_frame)
        self.populate_header()
        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid(row=0,column=0,padx=5,pady=5,sticky='w')

        self.scrollable = ctk.CTkScrollableFrame(self, corner_radius=0,fg_color="transparent")
        self.scrollable.grid_columnconfigure(0, weight=4)
        self.scrollable.grid_columnconfigure(1, weight=1)
        self.scrollable.grid_columnconfigure(2, weight=1)
        self.populate_table()
        self.scrollable.grid(row=1,column=0,padx=5,pady=5,sticky='nsew')

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

    def populate_table(self) -> None:
        start = time.time()
        for widget in self.scrollable.winfo_children():
            widget.destroy()

        files = self.controller.get_data_copy()
        logging.debug(f"populating table with {len(files)} files")
        if files.empty or files is None:
            label = ctk.CTkLabel(self.scrollable, text="No files detected! \n\n\nIf you expected files here, \nmake sure the Client Directory path in 'Settings' is correct.")
            label.grid(row=0,column=0,padx=8,pady=5,sticky='new')
            return

        #grabs the specified columns below, and
        self.clients = list(zip(files[FILE_NAME],files[STATUS],files[CLIENT_NAME]))
        self._populate_row_chunk(0)

        end = time.time()
        logging.debug(f"populate_table:{round(end-start,3)}s")

    def _populate_row_chunk(self, start_index:int, chunk_size=10, MAX_LENGTH=30) -> None:
        for i in range(start_index, min(start_index+chunk_size, len(self.clients))):
            client = self.clients[i]
            client_name = client[2]
            if client_name == DEFAULT_VALUES[CLIENT_NAME]:
                client_name = client[0]
            if len(client_name) > MAX_LENGTH:
                client_name = client_name[:MAX_LENGTH].rstrip() + "..."
            client_label = ctk.CTkLabel(self.scrollable, text=client_name, **style_label_body)
            client_label.grid(row=start_index+i, column=0, padx=(8, 0), pady=5, sticky='w')

            style = style_status_complete if client[1] else style_status_incomplete
            status_label = ctk.CTkLabel(self.scrollable, **style, corner_radius=5, width=50, justify="left", anchor="w")
            status_label.grid(row=start_index+i, column=1, pady=5, sticky='w')

            open_button = ctk.CTkButton(self.scrollable, text="Open File", **style_button, width=125,
                                        command=partial(self.open_file, self.controller.get_row(client[0])))
            open_button.grid(row=start_index+i, column=2, pady=5, sticky='w')

        if start_index + chunk_size < len(self.clients):
            self.after(10, self._populate_row_chunk, start_index + chunk_size)

    def open_file(self, file_data:FileData) -> None:
        inputOverlay = FileInput(self.controller, file_data, self, **style_sub_frame)

        start_y = 1.0
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
        target_y = 1.0
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
                widget.destroy()

        animate()
        self.update()

    def update(self) -> None:
        logging.debug("Refreshing the UI with updated data.")
        self.controller.update()
        self.populate_table()

    def sort(self) -> None:
        self.controller.sort_files()
        self.update()