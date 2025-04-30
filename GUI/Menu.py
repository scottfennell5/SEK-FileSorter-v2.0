import customtkinter as ctk

from Controller import Controller


class Menu(ctk.CTkFrame):
    def __init__(self, controller:Controller, master:ctk.CTkBaseClass, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)

        buttons = [
            ("Home", lambda : master.set_window("home")),
            #("Search", lambda : master.set_window("search")),
            ("Settings", lambda : master.set_window("settings")),
            ("Help", lambda : master.set_window("help"))
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

        for i, (text, cmd) in enumerate(buttons):
            (ctk.CTkButton(self, text=text, border_spacing=2, command=cmd, **BUTTON_STYLE)
            .grid(row=i, column=0, pady=20, sticky='ew'))