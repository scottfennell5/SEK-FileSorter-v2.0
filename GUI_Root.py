import customtkinter as ctk

from GUI.Home import Home
from GUI.Settings import Settings
from GUI.Help import Help

class FileSorter(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.current_window = None

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

        self.mainFrame = ctk.CTkFrame(self, fg_color="transparent")
        self.mainFrame.grid(row=0, column=1, padx=(0, 8), pady=8, sticky='nsew')
        self.setWindow("home")

    def getScreenCenterCords(self, root_width, root_height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - root_width) // 2
        y = (screen_height - root_height) // 2
        return [x, y]

    def setWindow(self,window):
        if window == self.current_window:
            pass
        else:
            for widget in self.mainFrame.winfo_children():
                widget.destroy()

            WINDOW_STYLE = {
                "fg_color":"#1E1E1E",
                "corner_radius":6
            }

            match window:
                case "home":
                    frame = Home(self.controller, self.mainFrame, **WINDOW_STYLE)
                case "settings":
                    frame = Settings(self.controller, self.mainFrame, **WINDOW_STYLE)
                case "help":
                    frame = Help(self.controller, self.mainFrame, **WINDOW_STYLE)
                case _:
                    exit(0)
            print(self.mainFrame.winfo_children())
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            self.current_window = window
            print(self.current_window)

class OptionsFrame(ctk.CTkFrame):
    def __init__(self, controller, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)

        buttons = [
            ("Home", lambda : master.setWindow("home")),
            ("Settings", lambda : master.setWindow("settings")),
            ("Help", lambda : master.setWindow("help"))
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