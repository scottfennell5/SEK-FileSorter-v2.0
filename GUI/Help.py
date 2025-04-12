import customtkinter as ctk

class Help(ctk.CTkFrame):
    def __init__(self, controller, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller

        self.label = ctk.CTkLabel(self,text=f"help")
        self.label.grid(row=0,column=0,sticky='ew')

        self.close_button1 = ctk.CTkButton(self, text="Save", command=lambda: self.controller.save_data())
        self.close_button1.grid(row=1, column=0, pady=10)
        self.close_button2 = ctk.CTkButton(self, text="Load", command=lambda: self.controller.load_data())
        self.close_button2.grid(row=1, column=1, pady=10)
        self.close_button3 = ctk.CTkButton(self, text="Check", command=lambda: self.controller.check_data())
        self.close_button3.grid(row=2, column=0, pady=10)
        self.close_button4 = ctk.CTkButton(self, text="Filter", command=lambda: self.controller.filter_data())
        self.close_button4.grid(row=2, column=1, pady=10)
        self.close_button4 = ctk.CTkButton(self, text="SaveSet", command=lambda: self.controller.save_settings())
        self.close_button4.grid(row=3, column=0, pady=10)
        self.close_button4 = ctk.CTkButton(self, text="LoadSet", command=lambda: self.controller.get_settings())
        self.close_button4.grid(row=3, column=1, pady=10)
        self.printrow = ctk.CTkButton(self, text="Print", command=lambda: self.controller.get_row("file1.pdf"))
        self.printrow.grid(row=4, column=0, pady=10)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)