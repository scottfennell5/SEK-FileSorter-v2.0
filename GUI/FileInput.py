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

        file_name = self.file_data[self.FILE_NAME]
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
        container = ctk.CTkFrame(tab, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        def create_labeled_entry(parent, label_text, placeholder):
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

        client1_frame = ctk.CTkFrame(container, fg_color="transparent")
        client1_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        client1_label = ctk.CTkLabel(client1_frame, text="Client 1", font=ctk.CTkFont(size=16, weight="bold"))
        client1_label.pack(anchor="w", pady=(0, 5))
        client1_first_entry = create_labeled_entry(client1_frame, "First name:", "Bob")
        client1_last_entry = create_labeled_entry(client1_frame, "Last name:", "Smith")

        radio_frame = ctk.CTkFrame(container, fg_color="transparent")
        radio_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        radio_label = ctk.CTkLabel(radio_frame, text="Is there another client?", width=100, anchor="w")
        radio_label.pack(side="left")
        radio_var = tk.IntVar(value=0)

        def radiobutton_event():
            if radio_var.get() == 1:
                client2_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
            else:
                client2_frame.grid_forget()

        ctk.CTkRadioButton(radio_frame, text="Yes", variable=radio_var, value=1,
                           command=radiobutton_event).pack(side="left", padx=10)
        ctk.CTkRadioButton(radio_frame, text="No", variable=radio_var, value=0,
                           command=radiobutton_event).pack(side="left", padx=10)

        client2_frame = ctk.CTkFrame(container, fg_color="transparent")
        client2_label = ctk.CTkLabel(client2_frame, text="Client 2", font=ctk.CTkFont(size=16, weight="bold"))
        client2_label.pack(anchor="w",pady=(0, 5))
        client2_first_entry = create_labeled_entry(client2_frame, "First name:", "Amanda")
        client2_last_entry = create_labeled_entry(client2_frame, "Last name:", "Smith")
        radio_var.set(0)

        misc_frame = ctk.CTkFrame(container, fg_color="transparent")
        misc_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        year_entry = create_labeled_entry(misc_frame, "Year:", "1984")
        file_desc_entry = create_labeled_entry(misc_frame, "File Description:", "Form 8879")

        #fill already completed entry labels
        client_type =   self.file_data[self.CLIENT_TYPE]
        client1_name =  self.file_data[self.CLIENT_NAME]
        client2_name =  self.file_data[self.CLIENT_NAME_2]
        year = self.file_data[self.YEAR]
        file_desc = self.file_data[self.DESCRIPTION]
        if client1_name != "unknown client" and client_type == "client":
            client1_first_entry.insert(0,client1_name.split(" ")[0])
            client1_last_entry.insert(0, client1_name.split(" ")[1])

        if client2_name is not None and client_type == "client":
            client2_first_entry.insert(0,client2_name.split(" ")[0])
            client2_last_entry.insert(0,client1_name.split(" ")[1])

        if year is not None:
            year_entry.insert(0,year)

        if file_desc is not None:
            file_desc_entry.insert(0,file_desc)

    def populate_business(self,tab):
        container = ctk.CTkFrame(tab, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=20)

        def create_labeled_entry(parent, label_text, placeholder):
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

        client1_frame = ctk.CTkFrame(container, fg_color="transparent")
        client1_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        client1_label = ctk.CTkLabel(client1_frame, text="Business 1", font=ctk.CTkFont(size=16, weight="bold"))
        client1_label.pack(anchor="w", pady=(0, 5))
        client1_entry = create_labeled_entry(client1_frame, "Business 1:", "Business LLC")

        radio_frame = ctk.CTkFrame(container, fg_color="transparent")
        radio_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=10)
        radio_label = ctk.CTkLabel(radio_frame, text="Is there another business?", width=100, anchor="w")
        radio_label.pack(side="left")
        radio_var = tk.IntVar(value=0)

        def radiobutton_event():
            if radio_var.get() == 1:
                client2_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)
            else:
                client2_frame.grid_forget()

        ctk.CTkRadioButton(radio_frame, text="Yes", variable=radio_var, value=1,
                           command=radiobutton_event).pack(side="left", padx=10)
        ctk.CTkRadioButton(radio_frame, text="No", variable=radio_var, value=0,
                           command=radiobutton_event).pack(side="left", padx=10)

        client2_frame = ctk.CTkFrame(container, fg_color="transparent")
        client2_label = ctk.CTkLabel(client2_frame, text="Client 2", font=ctk.CTkFont(size=16, weight="bold"))
        client2_label.pack(anchor="w", pady=(0, 5))
        client2_entry = create_labeled_entry(client2_frame, "Business 2:", "Another Business INC")
        radio_var.set(0)

        misc_frame = ctk.CTkFrame(container, fg_color="transparent")
        misc_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=10)
        year_entry = create_labeled_entry(misc_frame, "Year:", "1984")
        file_desc_entry = create_labeled_entry(misc_frame, "File Description:", "Form 8879")

        # fill already completed entry labels
        client_type = self.file_data[self.CLIENT_TYPE]
        client1_name = self.file_data[self.CLIENT_NAME]
        client2_name = self.file_data[self.CLIENT_NAME_2]
        year = self.file_data[self.YEAR]
        file_desc = self.file_data[self.DESCRIPTION]
        print(client1_name)
        print(client2_name)
        print(client1_name != "unknown client" and client_type == "business")
        print(client2_name is not None and client_type == "business")
        if client1_name != "unknown client" and client_type == "business":
            client1_entry.insert(0, client1_name)

        if client2_name is not None and client_type == "business":
            client2_entry.insert(0, client2_name)

        if year is not None:
            year_entry.insert(0, year)

        if file_desc is not None:
            file_desc_entry.insert(0, file_desc)

    def populate_footer(self):
        close_button = ctk.CTkButton(self.footer, text="Save Changes", width=125,
                                     fg_color="#C3B1E1", text_color="black", hover_color="#CCCCFF",
                                     command=lambda: self.save_changes())

        close_button.pack(side=ctk.RIGHT, padx=4, pady=5)

    def save_changes(self):
        #TODO
        #verify integrity of data
        #if passed, save and pass row changes to controller
        #if not, display error message with what needs fixed
        pass

    def open_file(self,file_name):
        self.controller.open_file(file_name)

    def close(self):
        if hasattr(self.master, 'close'):
            self.master.close(self)