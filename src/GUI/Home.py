import customtkinter as ctk
from functools import partial
import logging

from src.Controller import Controller
from src.GUI.FileInput import FileInput
from src.Utility.constants import FILE_NAME, STATUS, CLIENT_NAME, FileData, DEFAULT_VALUES


class Home(ctk.CTkFrame):
    def __init__(self, controller:Controller, master:ctk.CTkBaseClass, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.header = ctk.CTkFrame(self,corner_radius=5,fg_color="#1E1E1E")
        self.populate_header()
        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid(row=0,column=0,padx=5,pady=5,sticky='w')

        self.scrollable = ctk.CTkScrollableFrame(self, corner_radius=0,fg_color="#1E1E1E")
        self.scrollable.grid_columnconfigure(0, weight=4)
        self.scrollable.grid_columnconfigure(1, weight=1)
        self.scrollable.grid_columnconfigure(2, weight=1)
        self.populate_table()
        self.scrollable.grid(row=1,column=0,padx=5,pady=5,sticky='nsew')

    def populate_header(self) -> None:
        col = 0
        header_label = ctk.CTkLabel(self.header, text="Home",font=("Bold", 30),corner_radius=0,width=75,justify="left",anchor="w")
        header_label.pack(side=ctk.LEFT,padx=(8,150),pady=(5,2))
        col += 1

        button_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        button_frame.pack(side=ctk.RIGHT, fill="x",expand=True, padx=8, pady=(5,2))

        sort_button = ctk.CTkButton(button_frame, text="Sort", width=125,
                                    fg_color="#1E1E1E", text_color="#BB86FC", hover_color="#2E2E2E",
                                    command=lambda: self.sort())
        sort_button.pack(side=ctk.RIGHT, padx=4)
        col += 1

        refresh_button = ctk.CTkButton(button_frame, text="Refresh Data", width=125,
                                       fg_color="#1E1E1E", text_color="#BB86FC", hover_color="#2E2E2E",
                                       command=lambda : self.update())
        refresh_button.pack(side=ctk.RIGHT,padx=4)
        col += 1

    def populate_table(self) -> None:
        for widget in self.scrollable.winfo_children():
            widget.destroy()

        files = self.controller.get_data_copy()
        logging.debug(f"populating table with {len(files)} files")
        if files.empty or files is None:
            label = ctk.CTkLabel(self.scrollable, text="No files detected! \n\n\nIf you expected files here, \nmake sure the Client Directory path in 'Settings' is correct.")
            label.grid(row=0,column=0,padx=8,pady=5,sticky='new')
            return

        #grabs the specified columns below, and
        clients = list(zip(files[FILE_NAME],files[STATUS],files[CLIENT_NAME]))

        MAX_LENGTH = 30

        STATUS_COMPLETE_STYLE = {
            "text": "Complete",
            "fg_color": "#388E3C",
            "text_color": "#E0E0E0"
        }

        STATUS_INCOMPLETE_STYLE = {
            "text": "Incomplete",
            "fg_color": "#D97925",
            "text_color": "#E0E0E0"
        }

        row = 0
        for client in clients:
            #client = (file_name, status, client_name)
            client_name = client[2]
            if client_name == DEFAULT_VALUES[CLIENT_NAME]:
                client_name = client[0]
            if len(client_name) > MAX_LENGTH:
                client_name = client_name[:MAX_LENGTH].rstrip() + "..."
            client_label = ctk.CTkLabel(self.scrollable,text=client_name,corner_radius=0,width=75,
                                  text_color="#d1cfcf",
                                  justify="left",anchor="w")
            client_label.grid(row=row+1,column=0,padx=(8,0),pady=5,sticky='w')

            style = STATUS_COMPLETE_STYLE if client[1] else STATUS_INCOMPLETE_STYLE
            status_label = ctk.CTkLabel(self.scrollable, **style,corner_radius=5, width=50,justify="left", anchor="w")
            status_label.grid(row=row+1, column=1, pady=5, sticky='w')

            open_button = ctk.CTkButton(self.scrollable, text="Open File", width=125,
                                        fg_color="#2C2C2C", text_color="#BB86FC", hover_color="#2E2E2E",
                                        command=partial(self.open_file, self.controller.get_row(client[0])))
            open_button.grid(row=row+1,column=2,pady=5,sticky='w')

            row += 1

    def open_file(self, file_data:FileData) -> None:
        inputOverlay = FileInput(self.controller, file_data, self, fg_color="#1E1E1E", corner_radius=5)

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