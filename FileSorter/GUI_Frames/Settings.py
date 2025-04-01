import customtkinter as ctk

class Settings(ctk.CTkFrame):
    def __init__(self, controller, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label = ctk.CTkLabel(self,text=f"settings")
        self.label.grid(row=0,column=0,sticky='ew')

        self.close_button = ctk.CTkButton(self, text="Do Nothing", command=lambda: print('told u'))
        self.close_button.grid(row=1, column=0, pady=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)