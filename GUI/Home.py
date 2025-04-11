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
        header_label = ctk.CTkLabel(self.header, text="Home",font=("Bold", 30),corner_radius=0,width=75,justify="left",anchor="w")
        header_label.pack(side=ctk.LEFT,padx=(8,150),pady=(5,2))
        col += 1

        button_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        button_frame.pack(side=ctk.RIGHT, fill="x",expand=True, padx=8, pady=(5,2))

        sort_button = ctk.CTkButton(button_frame, text="Sort", width=125,
                                    fg_color="#1E1E1E", text_color="#BB86FC", hover_color="#2E2E2E",
                                    command=lambda: print("sorting"))
        sort_button.pack(side=ctk.RIGHT, padx=4)
        col += 1

        refresh_button = ctk.CTkButton(button_frame,text="Refresh Data",width=125,
                                    fg_color="#1E1E1E", text_color="#BB86FC", hover_color="#2E2E2E",
                                    command=lambda : self.controller.notifyObserver())
        refresh_button.pack(side=ctk.RIGHT,padx=4)
        col += 1

    def populateTable(self):
        for widget in self.scrollable.winfo_children():
            widget.destroy()

        files = self.controller.getDataCopy()
        print(f"files:{files}")
        if files.empty or files is None:
            label = ctk.CTkLabel(self.scrollable, text="No files detected! \n\n\nIf you expected files here, \nmake sure the Client Directory path in 'Settings' is correct.")
            label.grid(row=0,column=0,padx=8,pady=5,sticky='new')
            return

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

        #grabs the specified columns below, and
        clients = list(zip(files['First_Name'], files['File_Status'], files['File_Name']))

        NAME=0
        STATUS=1
        FILE_NAME=2

        row = 0
        col = 0
        for client in clients:

            client_name = client[NAME]
            if len(client_name) > MAX_LENGTH:
                client_name = client_name[:MAX_LENGTH].rstrip() + "..."
            client_label = ctk.CTkLabel(self.scrollable,text=client_name,corner_radius=0,width=75,
                                  text_color="#d1cfcf",
                                  justify="left",anchor="w")
            client_label.grid(row=row+1,column=col,padx=(8,0),pady=5,sticky='w')
            col+=1

            status = client[STATUS]
            style = STATUS_COMPLETE_STYLE if client[STATUS] else STATUS_INCOMPLETE_STYLE
            status_label = ctk.CTkLabel(self.scrollable, **style,corner_radius=5, width=50,justify="left", anchor="w")
            status_label.grid(row=row+1, column=col, pady=5, sticky='w')
            col+=1

            open_button = ctk.CTkButton(self.scrollable,text="Open File",width=125,
                                        fg_color="#1E1E1E",text_color="#BB86FC",hover_color="#2E2E2E",
                                        command=partial(self.openFile, client[FILE_NAME]))
            open_button.grid(row=row+1,column=col,pady=5,sticky='w')
            col += 1

            col = 0
            row += 1

    def openFile(self, file_name):
        inputOverlay = FileInput(self.controller,file_name,self)
        inputOverlay.place(relx=0, rely=0, relwidth=1, relheight=1)
        inputOverlay.lift()

    def update(self):
        print("Refreshing the UI with updated data.")
        print(f"self: {self}")
        print(f"selfID: {id(self)}")
        print("-------------------------")
        self.populateTable()

class FileInput(ctk.CTkFrame):
    def __init__(self, controller, file_name, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header = ctk.CTkFrame(self, corner_radius=5, fg_color="#1E1E1E")
        self.header.grid(row=0, column=0, pady=(8, 4), sticky='nw')
        self.populateHeader()

        self.body = ctk.CTkFrame(self, corner_radius=5, fg_color="transparent")
        self.body.grid(row=1, column=0, sticky='nsew')
        self.body.columnconfigure(0, weight=0)
        self.body.columnconfigure(1, weight=1)
        self.body.columnconfigure(2, weight=0)
        self.populateBody()

    def populateHeader(self):
        pass

    def populateBody(self):
        pass

    def saveChanges(self):
        pass

    def close(self):
        self.destroy()
