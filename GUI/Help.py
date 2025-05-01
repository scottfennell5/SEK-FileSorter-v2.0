import customtkinter as ctk

class Help(ctk.CTkFrame):
    def __init__(self, controller, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller

        self.label = ctk.CTkLabel(self,text=f"help")
        self.label.grid(row=0,column=0,sticky='ew')