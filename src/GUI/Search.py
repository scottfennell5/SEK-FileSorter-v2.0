import customtkinter as ctk

from Core.Controller import Controller


class Search(ctk.CTkFrame):
    def __init__(self, controller:Controller, master:ctk.CTkBaseClass, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller

        self.label = ctk.CTkLabel(self, text=f"Under construction, come back later")
        self.label.grid(row=0, column=0, sticky='ew')