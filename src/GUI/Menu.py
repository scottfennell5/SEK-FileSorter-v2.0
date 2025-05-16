import customtkinter as ctk
from customtkinter import CTkBaseClass

from Core.Controller import Controller
from Utility.style import style_main_menu_button


class Menu(ctk.CTkFrame):
    def __init__(self, master:CTkBaseClass, controller:Controller, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)

        buttons = [
            ("Home", lambda : master.set_window("home")),
            #("Search", lambda : master.set_window("search")),
            ("Settings", lambda : master.set_window("settings")),
            ("Help", lambda : master.set_window("help"))
        ]

        for i, (text, cmd) in enumerate(buttons):
            (ctk.CTkButton(self, text=text, **style_main_menu_button, command=cmd)
            .grid(row=i, column=0, pady=20, sticky='ew'))