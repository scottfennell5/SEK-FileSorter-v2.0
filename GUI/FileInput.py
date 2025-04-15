import customtkinter as ctk
import tkinter as tk

class FileInput(ctk.CTkFrame):
    FILE_NAME = 0
    STATUS = 1
    CLIENT_TYPE = 2
    CLIENT_NAME = 3
    CLIENT_NAME_2 = 4
    YEAR = 5
    DESCRIPTION = 6

    def __init__(self, controller, file_data, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.file_data_original = file_data
        self.file_data = file_data
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header = ctk.CTkFrame(self,corner_radius=0,fg_color="transparent")
        self.header.grid(row=0,column=0,pady=(8, 4),sticky='new')
        self.populate_header()

        self.body = ctk.CTkFrame(self, corner_radius=0,fg_color="transparent")
        self.body.grid(row=1,column=0,sticky='nsew')
        self.body.columnconfigure(0, weight=0)
        self.body.columnconfigure(1, weight=1)
        self.body.columnconfigure(2, weight=0)
        self.populate_body()

    def populate_header(self):
        file_name = self.file_data[self.FILE_NAME]
        header_label = ctk.CTkLabel(self.header,text=file_name,
                                    font=("Bold", 30),corner_radius=0,width=75,
                                    fg_color="transparent",justify="left",anchor="w")
        header_label.pack(side=ctk.LEFT,padx=(8, 0),pady=(5, 2))

        open_file_button = ctk.CTkButton(self.header, text="Open PDF", width=125,
                                     fg_color="#1E1E1E", text_color="#BB86FC", hover_color="#2E2E2E",
                                     command=lambda: self.open_file(file_name))

        close_button = ctk.CTkButton(self.header, text="Close", width=125,
                                     fg_color="#CBC3E3", text_color="black", hover_color="#2E2E2E",
                                     command=lambda: self.close())

        close_button.pack(side=ctk.RIGHT, padx=4, pady=5)
        open_file_button.pack(side=ctk.RIGHT, padx=4, pady=5)

    def populate_body(self):
        tab_view = ctk.CTkTabview(self.body,fg_color="#1A1A1A", corner_radius=0)
        tab_view.pack(fill="both",expand=True)
        tab_client = tab_view.add("Client")
        tab_business = tab_view.add("Business")
        try:
            tab_view.set(self.file_data[self.CLIENT_TYPE])
        except ValueError:
            tab_view.set("Client")

        self.populate_client(tab_client)
        tab_client.columnconfigure(1,weight=1)
        tab_client.columnconfigure(3, weight=1)
        self.populate_business(tab_business)

    def populate_client(self, tab):
        name_1_header = ctk.CTkLabel(tab, text="Client 1")
        name_1_header.grid(row=0, column=0)
        name_1_first_label = ctk.CTkLabel(tab, text="First name: ")
        name_1_first_label.grid(row=1, column=0)
        name_1_first_entry = ctk.CTkEntry(tab, placeholder_text="Bob")
        name_1_first_entry.grid(row=1, column=1)
        name_1_last_label = ctk.CTkLabel(tab, text="Last name: ")
        name_1_last_label.grid(row=1, column=2)
        name_1_last_entry = ctk.CTkEntry(tab, placeholder_text="Smith")
        name_1_last_entry.grid(row=1, column=3)

        def radiobutton_event():
            if name_2_radio_var.get() == 1:
                name_2_frame.grid(row=3, column=0, columnspan=4)
            else:
                name_2_frame.grid_forget()

        name_2_radio_label = ctk.CTkLabel(tab, text="Client 2?")
        name_2_radio_label.grid(row=2, column=0)
        name_2_radio_var = tk.IntVar(value=0)
        name_2_radio_yes = ctk.CTkRadioButton(tab, text="Yes",
                                              command=radiobutton_event, variable=name_2_radio_var, value=1)
        name_2_radio_yes.grid(row=2, column=1)
        name_2_radio_no = ctk.CTkRadioButton(tab, text="No",
                                             command=radiobutton_event, variable=name_2_radio_var, value=0)
        name_2_radio_no.grid(row=2, column=2)
        name_2_radio_no.select()

        name_2_frame = ctk.CTkFrame(tab, fg_color="transparent")
        # name_2_frame.grid(row=3, column=0, columnspan=5)
        name_2_header = ctk.CTkLabel(name_2_frame, text="Client 2")
        name_2_header.grid(row=0, column=0)
        name_2_first_label = ctk.CTkLabel(name_2_frame, text="First name: ")
        name_2_first_label.grid(row=1, column=0)
        name_2_first_entry = ctk.CTkEntry(name_2_frame, placeholder_text="Amanda")
        name_2_first_entry.grid(row=1, column=1)
        name_2_last_label = ctk.CTkLabel(name_2_frame, text="Last name: ")
        name_2_last_label.grid(row=1, column=2)
        name_2_last_entry = ctk.CTkEntry(name_2_frame, placeholder_text="Smith")
        name_2_last_entry.grid(row=1, column=3)

        year_label = ctk.CTkLabel(tab, text="Year:")
        year_label.grid(row=4, column=0)
        year_entry = ctk.CTkEntry(tab, placeholder_text="1984")
        year_entry.grid(row=4, column=1)

        description_label = ctk.CTkLabel(tab, text="File Description:")
        description_label.grid(row=5, column=0)
        description_entry = ctk.CTkEntry(tab, placeholder_text="Form 8879")
        description_entry.grid(row=5, column=1)

    def populate_business(self,tab):
        business_name_header = ctk.CTkLabel(tab, text="Business 1")
        business_name_header.grid(row=0, column=0)

        business_name_label = ctk.CTkLabel(tab, text="Business name: ")
        business_name_label.grid(row=1, column=0)
        business_name_entry = ctk.CTkEntry(tab, placeholder_text="'Business INC' or 'Business LLC'",width=300)
        business_name_entry.grid(row=1, column=1)

        year_label = ctk.CTkLabel(tab, text="Year:",)
        year_label.grid(row=2, column=0)
        year_entry = ctk.CTkEntry(tab, placeholder_text="1984",width=100)
        year_entry.grid(row=2, column=1)

        description_label = ctk.CTkLabel(tab, text="File Description:")
        description_label.grid(row=3, column=0)
        description_entry = ctk.CTkEntry(tab, placeholder_text="Form 8879",width=300)
        description_entry.grid(row=3, column=1)

    def save_changes(self):
        pass

    def open_file(self,file_name):
        self.controller.open_file(file_name)

    def close(self):
        if hasattr(self.master, 'close'):
            self.master.close(self)