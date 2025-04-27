import logging

import customtkinter as ctk
import tkinter as tk

from Utility.constants import (
    FILE_NAME, STATUS, CLIENT_TYPE, CLIENT_NAME, CLIENT_NAME_2, YEAR, DESCRIPTION,
    CLIENT, BUSINESS)

class FileInput(ctk.CTkFrame):
    CLIENT = "Client"
    BUSINESS = "Business"

    RADIO_VAR = "radiovar"

    SAMPLE_DATA = {
        CLIENT: {
            CLIENT_NAME: "Bob Smith",
            CLIENT_NAME_2: "Amanda Smith"
        },
        BUSINESS: {
            CLIENT_NAME: "BUSINESS LLC",
            CLIENT_NAME_2: "ANOTHER BUSINESS INC"
        }
    }

    def __init__(self, controller, file_data, master, **kwargs):
        super().__init__(master, **kwargs)
        logging.debug(f"Creating FileInput object with data: {file_data}")
        self.controller = controller
        self.file_data_original = file_data
        self.file_data = file_data
        self.entries = {
            self.CLIENT: {},
            self.BUSINESS: {}
        }
        self.status_label = None
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0,weight=0)
        self.grid_rowconfigure(1,weight=1)
        self.grid_rowconfigure(2,weight=0)

        self.header = ctk.CTkFrame(self,corner_radius=0,fg_color="transparent")
        self.header.grid(row=0,column=0,pady=(8, 4),sticky='new')
        self.populate_header()

        self.body = ctk.CTkFrame(self,corner_radius=0,fg_color="transparent")
        self.body.grid(row=1,column=0,sticky='nsew')
        self.populate_body()

        self.footer = ctk.CTkFrame(self,corner_radius=0,fg_color="transparent")
        self.footer.grid(row=2,column=0,padx=4,pady=4,sticky='ew')
        self.populate_footer()

    def populate_header(self):
        MAX_LENGTH = 15

        file_name = self.file_data[FILE_NAME]
        if len(file_name) > MAX_LENGTH:
            file_name = file_name[:MAX_LENGTH].rstrip() + "..."
        header_label = ctk.CTkLabel(self.header,text=file_name,
                                    font=("Bold",30),corner_radius=0,width=75,
                                    fg_color="transparent",justify="left",anchor="w")
        header_label.pack(side=ctk.LEFT,padx=(8, 0),pady=(5, 2))

        open_file_button = ctk.CTkButton(self.header, text="Open PDF", width=125,
                                     fg_color="#1E1E1E", text_color="#BB86FC", hover_color="#2E2E2E",
                                     command=lambda: self.open_file(file_name))

        close_button = ctk.CTkButton(self.header, text="Close", width=125,
                                     fg_color="#C3B1E1", text_color="black", hover_color="#CCCCFF",
                                     command=lambda: self.close())

        close_button.pack(side=ctk.RIGHT, padx=4, pady=5)
        open_file_button.pack(side=ctk.RIGHT, padx=4, pady=5)

    def populate_body(self):
        self.tab_view = ctk.CTkTabview(self.body,fg_color="#1A1A1A", corner_radius=0)
        self.tab_view.pack(fill="both",expand=True)
        tab_client = self.tab_view.add(CLIENT)
        tab_business = self.tab_view.add(BUSINESS)
        try:
            self.tab_view.set(self.file_data[CLIENT_TYPE])
        except ValueError as e:
            logging.warning(f"ValueError, client type likely still default:\n{e}")
            self.tab_view.set(self.CLIENT)

        self.populate_tab(tab_client, self.CLIENT)
        tab_client.columnconfigure(1,weight=1)
        tab_client.columnconfigure(3, weight=1)
        self.populate_tab(tab_business, self.BUSINESS)

    def create_labeled_entry(self, parent, label_text, placeholder):
        """
            Label_text: [placeholder   ]
        """
        row = ctk.CTkFrame(parent, fg_color="transparent")
        row.pack(fill="x", pady=5)
        label = ctk.CTkLabel(row, text=label_text, width=100, anchor="w")
        label.pack(side="left")
        entry = ctk.CTkEntry(row, placeholder_text=placeholder)
        entry.pack(side="left", fill="x", expand=True, padx=(10, 0))
        return entry

    def populate_tab(self, tab, tab_type):
        container = ctk.CTkFrame(tab, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        client1_frame = ctk.CTkFrame(container, fg_color="transparent")
        client1_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        client1_label = ctk.CTkLabel(client1_frame, text="Client 1", font=ctk.CTkFont(size=16, weight="bold"))
        client1_label.pack(anchor="w", pady=(0, 5))
        entry = self.create_labeled_entry(client1_frame, "Name:", self.SAMPLE_DATA[tab_type][CLIENT_NAME])
        self.entries[tab_type][CLIENT_NAME] = entry

        radio_frame = ctk.CTkFrame(container, fg_color="transparent")
        radio_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        radio_label = ctk.CTkLabel(radio_frame, text="Is there another client?", width=100, anchor="w")
        radio_label.pack(side="left")
        radio_var = tk.IntVar(value=0)
        self.entries[tab_type][self.RADIO_VAR] = radio_var

        def radiobutton_event():
            if self.entries[tab_type][self.RADIO_VAR].get() == 1:
                client2_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
            else:
                client2_frame.grid_forget()

        ctk.CTkRadioButton(radio_frame, text="Yes", variable=self.entries[tab_type][self.RADIO_VAR], value=1,
                           command=radiobutton_event).pack(side="left", padx=10)
        ctk.CTkRadioButton(radio_frame, text="No", variable=self.entries[tab_type][self.RADIO_VAR], value=0,
                           command=radiobutton_event).pack(side="left", padx=10)

        client2_frame = ctk.CTkFrame(container, fg_color="transparent")
        client2_label = ctk.CTkLabel(client2_frame, text="Client 2", font=ctk.CTkFont(size=16, weight="bold"))
        client2_label.pack(anchor="w", pady=(0, 5))
        entry = self.create_labeled_entry(client2_frame, "Name:", self.SAMPLE_DATA[tab_type][CLIENT_NAME_2])
        self.entries[tab_type][CLIENT_NAME_2] = entry

        misc_frame = ctk.CTkFrame(container, fg_color="transparent")
        misc_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        entry = self.create_labeled_entry(misc_frame, "Year:", "1984")
        self.entries[tab_type][YEAR] = entry
        entry = self.create_labeled_entry(misc_frame, "File Description:", "Form 8879")
        self.entries[tab_type][DESCRIPTION] = entry

        # fill already completed entry labels
        client1_name = self.file_data[CLIENT_NAME]
        client2_name = self.file_data[CLIENT_NAME_2]
        year = self.file_data[YEAR]
        file_desc = self.file_data[DESCRIPTION]

        if client1_name != "unknown client":
            self.entries[tab_type][CLIENT_NAME].insert(0, client1_name)

        if client2_name is not None:
            self.entries[tab_type][CLIENT_NAME_2].insert(0, client2_name)
            self.entries[tab_type][self.RADIO_VAR].set(1)
        else:
            self.entries[tab_type][self.RADIO_VAR].set(0)
        radiobutton_event()

        if year != -1:
            self.entries[tab_type][YEAR].insert(0, year)

        if file_desc is not None:
            self.entries[tab_type][DESCRIPTION].insert(0, file_desc)

    def populate_footer(self):
        close_button = ctk.CTkButton(self.footer, text="Save Changes", width=125,
                                     fg_color="#C3B1E1", text_color="black", hover_color="#CCCCFF",
                                     command=lambda: self.save_changes(self.tab_view.get()))

        close_button.pack(side=ctk.RIGHT, padx=4, pady=5)

    def save_changes(self, tab_type):
        self.file_data = {
            FILE_NAME:self.file_data_original[FILE_NAME],
            STATUS:self.file_data_original[STATUS],
            CLIENT_TYPE:self.tab_view.get(),
            CLIENT_NAME:self.entries[tab_type][CLIENT_NAME].get(),
            CLIENT_NAME_2:self.entries[tab_type][CLIENT_NAME_2].get(),
            YEAR:self.entries[tab_type][YEAR].get(),
            DESCRIPTION:self.entries[tab_type][DESCRIPTION].get()
        }
        errors = self.controller.save_row_changes(self.file_data, self.entries[tab_type][self.RADIO_VAR].get())
        if self.status_label:
            self.status_label.destroy()
        if not errors:
            self.status_label = ctk.CTkLabel(self.footer,
                                             text=f"*Data is valid and has been saved.\nYou can safely close this window.",
                                             text_color="#90EE90")
            self.status_label.pack(side=ctk.LEFT)
        else:
            self.status_label = ctk.CTkLabel(self.footer,
                                              text=f"*Data saved, but the following fields are empty or incorrect:\n{errors}",
                                              text_color="#FFD7D7")
            self.status_label.pack(side=ctk.LEFT)

    def open_file(self,file_name):
        self.controller.open_file(file_name)

    def close(self):
        if hasattr(self.master, 'close'):
            self.master.close(self)