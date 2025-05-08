from tkinter import messagebox
import customtkinter as ctk
import logging

from Core.Controller import Controller
from GUI.Menu import Menu
from GUI.Home import Home
from GUI.Settings import Settings
from GUI.Help import Help
from Utility.style import style_sub_frame

class FileSorter(ctk.CTk):
    def __init__(self, controller:Controller):
        super().__init__()
        self.controller = controller
        self.current_window = None

        width = 800
        height = 650
        center = self.get_screen_center_cords(width, height)
        self.geometry(f'{width}x{height}+{center[0]}+{center[1]}')
        self.resizable(False, False)
        self.title('SEK File Sorter v2.0')
        self.configure(fg_color="#121212")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)

        self.menuFrame = Menu(controller, self, **style_sub_frame)
        self.menuFrame.grid(row=0, column=0, padx=8, pady=8, sticky='nsew')

        self.mainFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.mainFrame.grid(row=0, column=1, padx=(0, 8), pady=8, sticky='nsew')
        self.set_window("home")

    def report_callback_exception(self, exc, val, tb):
        """
        Overrides the default exception handler in customTkinter so all errors can be logged.
        Since unhandled errors can cause the program to be stuck in a loop, the
        application will destroy itself in the case that an unexpected error occurs.
        """
        logging.fatal(f"Unhandled GUI Exception: ", exc_info=(exc, val, tb))
        messagebox.showerror("Fatal Error", "A fatal error occurred. The application will now close.")
        self.destroy()

    def get_screen_center_cords(self, root_width:int, root_height:int) -> tuple[int,int]:
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - root_width) // 2
        y = (screen_height - root_height) // 2
        return x,y

    def set_window(self, window:str) -> None:
        if window == self.current_window:
            return

        for widget in self.mainFrame.winfo_children():
            widget.destroy()

        match window:
            case "home":
                frame = Home(self.controller, self.mainFrame, **style_sub_frame)
            case "settings":
                frame = Settings(self.controller, self.mainFrame, **style_sub_frame)
            case "help":
                frame = Help(self.controller, self.mainFrame, **style_sub_frame)
            case _:
                exit(0)
        logging.debug(self.mainFrame.winfo_children())
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.current_window = window
        logging.debug(self.current_window)