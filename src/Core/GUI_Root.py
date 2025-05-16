from tkinter import messagebox
import customtkinter as ctk
import logging

from Core.Controller import Controller
from GUI.Menu import Menu
from GUI.Home import Home
from GUI.Settings import Settings
from GUI.Help import Help
from Utility.constants import HOME_ID, SETTINGS_ID, HELP_ID
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

        self.menu_frame = Menu(self, controller, **style_sub_frame)
        self.menu_frame.grid(row=0, column=0, padx=8, pady=8, sticky='nsew')

        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, padx=(0, 8), pady=8, sticky='nsew')

        self.home_frame = Home(self.main_frame, self.controller, **style_sub_frame)
        self.settings_frame = Settings(self.controller, self.main_frame, **style_sub_frame)
        self.help_frame = Help(self.controller, self.main_frame, **style_sub_frame)

        self.frames = {
            HOME_ID:self.home_frame,
            SETTINGS_ID:self.settings_frame,
            HELP_ID:self.help_frame
        }

        self.set_window(HOME_ID)

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

        if self.current_window:
            self.frames[self.current_window].place_forget()

        new_frame = self.frames.get(window)
        if not new_frame:
            raise ValueError(f"Unknown window: {window}")

        new_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.current_window = window