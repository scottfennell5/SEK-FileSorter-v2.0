import customtkinter as ctk
from functools import partial

class Home(ctk.CTkFrame):
    def __init__(self, controller, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.controller.newObserver(self)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.header = ctk.CTkFrame(self,corner_radius=5,fg_color="#1E1E1E")
        self.populateHeader()
        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid(row=0,column=0,padx=5,pady=5,sticky='w')

        self.scrollable = ctk.CTkScrollableFrame(self, corner_radius=0,fg_color="#1E1E1E")
        self.populateTable()
        self.scrollable.grid_columnconfigure(0, weight=3)
        self.scrollable.grid_columnconfigure(1, weight=1)
        self.scrollable.grid_columnconfigure(2, weight=1)
        self.scrollable.grid(row=1,column=0,padx=5,pady=5,sticky='nsew')

    def populateHeader(self):
        col = 0
        header_label = ctk.CTkLabel(self.header, text=f"Files",font=("Bold", 20),corner_radius=0,width=75,justify="left",anchor="w")
        header_label.pack(side=ctk.LEFT,padx=(8,0),pady=(5,2))
        col += 1

        button_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        button_frame.pack(side=ctk.RIGHT, fill="x",expand=True, padx=8, pady=(5,2))

        sort_button = ctk.CTkButton(button_frame, text="Sort", width=125,
                                    fg_color="#1E1E1E", text_color="#BB86FC", hover_color="#2E2E2E",
                                    command=lambda: print("sorting"))
        sort_button.pack(side=ctk.RIGHT, padx=4)
        col += 1

        open_button = ctk.CTkButton(button_frame,text="Refresh Data",width=125,
                                    fg_color="#1E1E1E", text_color="#BB86FC", hover_color="#2E2E2E",
                                    command=lambda : self.controller.notifyObservers())
        open_button.pack(side=ctk.RIGHT,padx=4)
        col += 1

    def populateTable(self):
        print("populateTable() called")
        print(f"self: {self}")
        print(f"selfID: {id(self)}")
        print(f"self.scrollable: {self.scrollable}")
        print(f"self.scrollable.winfo_children(): {self.scrollable.winfo_children()}")
        for widget in self.scrollable.winfo_children():
            widget.destroy()
        print(f"self.scrollable.winfo_children(): {self.scrollable.winfo_children()}")
        MAX_LENGTH = 30
        files = self.controller.getFiles()
        col = 0

        STATUS_READY_STYLE = {
            "text": "Ready",
            "fg_color": "#388E3C",
            "text_color": "#E0E0E0"
        }

        STATUS_NOT_READY_STYLE = {
            "text": "Not Ready",
            "fg_color": "#D97925",
            "text_color": "#E0E0E0"
        }

        for row in files.itertuples():
            """
            #TESTING PURPOSES ONLY
            file_name = row.File_Name
            if len(file_name) > MAX_LENGTH:
                file_name = file_name[:MAX_LENGTH].rstrip() + "..."
            file_label = ctk.CTkLabel(parent,text=file_name,corner_radius=0,justify="left",anchor="w")
            file_label.grid(row=row.Index+1,column=col,padx=(5,0),pady=5,sticky='w')
            col+=1
            """

            client_name = row.First_Name
            if len(client_name) > MAX_LENGTH:
                client_name = client_name[:MAX_LENGTH].rstrip() + "..."
            client = ctk.CTkLabel(self.scrollable,text=client_name,corner_radius=0,width=75,
                                  text_color="#d1cfcf",
                                  justify="left",anchor="w")
            client.grid(row=row.Index+1,column=col,padx=(8,0),pady=5,sticky='w')
            col+=1

            style = STATUS_READY_STYLE if row.File_Status else STATUS_NOT_READY_STYLE
            status_label = ctk.CTkLabel(self.scrollable, **style,corner_radius=5, width=50,justify="left", anchor="w")
            status_label.grid(row=row.Index + 1, column=col, pady=5, sticky='w')
            col+=1

            open_button = ctk.CTkButton(self.scrollable,text="Open File",width=125,
                                        fg_color="#1E1E1E",text_color="#BB86FC",hover_color="#2E2E2E",
                                        command=partial(self.openFile, row.File_Name))
            open_button.grid(row=row.Index+1,column=col,pady=5,sticky='w')
            col += 1

            col = 0

    def openFile(self, file_name):
        inputOverlay = FileInput(self.controller,file_name,self)
        inputOverlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        inputOverlay.lift()

    def update(self):
        #update table with new data
        print("Refreshing the UI with updated data.")
        print(f"self: {self}")
        print(f"selfID: {id(self)}")
        self.populateTable()

class FileInput(ctk.CTkFrame):
    def __init__(self, controller, file_name, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label = ctk.CTkLabel(self,text=f"file: {file_name}")
        self.label.grid(row=0,column=0,sticky='ew')

        self.close_button = ctk.CTkButton(self, text="Do Nothing", command=self.close)
        self.close_button.grid(row=1, column=0, pady=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def close(self):
        self.destroy()
