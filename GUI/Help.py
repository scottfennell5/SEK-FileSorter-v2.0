import customtkinter as ctk

class Help(ctk.CTkFrame):
    def __init__(self, controller, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller

        self.label = ctk.CTkLabel(self,text=f"help")
        self.label.grid(row=0,column=0,sticky='ew')

        self.close_button1 = ctk.CTkButton(self, text="Save", command=lambda: self.controller.saveData())
        self.close_button1.grid(row=1, column=0, pady=10)
        self.close_button2 = ctk.CTkButton(self, text="Load", command=lambda: self.controller.loadData())
        self.close_button2.grid(row=1, column=1, pady=10)
        self.close_button3 = ctk.CTkButton(self, text="Check", command=lambda: self.controller.checkData())
        self.close_button3.grid(row=2, column=0, pady=10)
        self.close_button4 = ctk.CTkButton(self, text="Filter", command=lambda: self.controller.filterData())
        self.close_button4.grid(row=2, column=1, pady=10)
        self.close_button4 = ctk.CTkButton(self, text="SaveSet", command=lambda: self.controller.saveSettings())
        self.close_button4.grid(row=3, column=0, pady=10)
        self.close_button4 = ctk.CTkButton(self, text="LoadSet", command=lambda: self.controller.getSettings())
        self.close_button4.grid(row=3, column=1, pady=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)