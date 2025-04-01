import customtkinter as ctk
from customtkinter import CTkScrollableFrame
from functools import partial

from FileSorter_Sorter import Sorter
from FileSorter_DataHandler import DataHandler
from FileSorter_Controller import Controller

class FileSorter(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller

        width = 800
        height = 650
        center = self.getScreenCenterCords(width, height)
        self.geometry(f'{width}x{height}+{center[0]}+{center[1]}')
        self.resizable(False, False)
        self.title('SEK File Sorter v2.0')
        self.configure(fg_color="#121212")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        self.optionsFrame = OptionsFrame(controller,self,fg_color="#1E1E1E",corner_radius=6)
        self.optionsFrame.grid(row=0,column=0,padx=8,pady=8,sticky='nsew')

        self.mainFrame = MainFrame(controller, self, fg_color="#1E1E1E",corner_radius=6)
        self.mainFrame.grid(row=0,column=1,padx=(0,8),pady=8,sticky='nsew')

    def getScreenCenterCords(self, root_width, root_height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - root_width) // 2
        y = (screen_height - root_height) // 2
        return [x, y]

class OptionsFrame(ctk.CTkFrame):
    def __init__(self, controller, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)
        self.current_window = "main"

        buttons = [
            ("Home", lambda : print("home")),
            ("Settings", lambda : print("settings")),
            ("Help", lambda : print("help"))
        ]

        BUTTON_STYLE = {
            "font": ("Bold", 40),
            "corner_radius": 0,
            "height": 50,
            "anchor": "w",
            "fg_color": "#1E1E1E",
            "bg_color": "transparent",
            "text_color": "#d1cfcf",
            "hover_color": "#7e4694"
        }

        """
        green: 006400
        purple: 6e487d
        """

        for i, (text, cmd) in enumerate(buttons):
            (ctk.CTkButton(self, text=text, border_spacing=2, command=cmd, **BUTTON_STYLE)
            .grid(row=i, column=0, pady=20, sticky='ew'))

class MainFrame(ctk.CTkFrame):
    def __init__(self, controller, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.controller.addObserver(self)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.header = ctk.CTkFrame(self,corner_radius=5,fg_color="#1E1E1E")
        self.populateHeader(self.header)
        self.header.grid_columnconfigure(0, weight=1)
        self.header.grid(row=0,column=0,padx=5,pady=5,sticky='w')

        self.scrollable = CTkScrollableFrame(self, corner_radius=0,fg_color="#1E1E1E")
        self.populateTable(self.scrollable)
        self.scrollable.grid_columnconfigure(0, weight=3)
        self.scrollable.grid_columnconfigure(1, weight=1)
        self.scrollable.grid_columnconfigure(2, weight=1)
        self.scrollable.grid(row=1,column=0,padx=5,pady=5,sticky='nsew')

    def populateHeader(self,parent):
        col = 0
        """
        #TESTING PURPOSES ONLY
        file_label = ctk.CTkLabel(header,text="File Name",font=("Bold", 20),corner_radius=0,width=75,justify="left",anchor="w")
        file_label.grid(row=0,column=col,padx=(5,0),pady=5,sticky='w')
        col += 1
        """
        header_label = ctk.CTkLabel(parent, text=f"Files",font=("Bold", 20),corner_radius=0,width=75,justify="left",anchor="w")
        header_label.pack(side=ctk.LEFT,padx=(8,0),pady=(5,2))
        col += 1

        button_frame = ctk.CTkFrame(parent, fg_color="transparent")
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

    def populateTable(self,parent):
        for widget in parent.winfo_children():
            widget.destroy()

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
            client = ctk.CTkLabel(parent,text=client_name,corner_radius=0,width=75,
                                  text_color="#d1cfcf",
                                  justify="left",anchor="w")
            client.grid(row=row.Index+1,column=col,padx=(8,0),pady=5,sticky='w')
            col+=1

            style = STATUS_READY_STYLE if row.File_Status else STATUS_NOT_READY_STYLE
            status_label = ctk.CTkLabel(parent, **style,corner_radius=5, width=50,justify="left", anchor="w")
            status_label.grid(row=row.Index + 1, column=col, pady=5, sticky='w')
            col+=1

            open_button = ctk.CTkButton(parent,text="Open File",width=125,
                                        fg_color="#1E1E1E",text_color="#BB86FC",hover_color="#2E2E2E",
                                        command=partial(self.openFile, row.File_Name))
            open_button.grid(row=row.Index+1,column=col,pady=5,sticky='w')
            col += 1

            col = 0

    def openFile(self, file_name):
        print(f"open {file_name}")

    def update(self):
        #update table with new data
        print("Refreshing the UI with updated data.")
        self.populateTable(self.scrollable)

if __name__ == '__main__':
    dataHandler = DataHandler()
    sorter = Sorter()

    controller = Controller(dataHandler, sorter)

    program = FileSorter(controller)
    program.mainloop()