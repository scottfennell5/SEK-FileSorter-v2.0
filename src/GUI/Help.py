import customtkinter as ctk
from Utility.style import (
    style_label_header,
    style_label_body_header,
    style_label_body,
    style_invisible_frame
)


class Help(ctk.CTkFrame):
    def __init__(self, controller, master, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1,weight=1)

        self.header = ctk.CTkFrame(self, **style_invisible_frame)
        self.header.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.label = ctk.CTkLabel(self.header, text="Help", **style_label_header)
        self.label.pack(side=ctk.LEFT)

        self.body = ctk.CTkScrollableFrame(self, **style_invisible_frame)
        self.body.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.body.columnconfigure(0, weight=1)

        self.body_labels = []

        def update_wraplengths():
            wrap_length = self.master.winfo_width() - 200
            print(wrap_length)
            for label in self.body_labels:
                label.configure(wraplength=wrap_length)

        # --- Reserved: Getting Started ------------------------------------------------------------------------
        getting_started_header = ctk.CTkLabel(self.body, text="Getting Started", **style_label_body_header)
        getting_started_header.grid(row=0, column=0, padx=5, pady=(10, 2), sticky='w')

        getting_started_body = ctk.CTkLabel(self.body, **style_label_body,
            text=(
                "1.)Visit the 'Settings' page to ensure the scanned and target directories are set correctly.\n"
                "2.)Navigate to the 'Home' menu to see the list of files pulled from the provided scan directory.\n"
                "3.)Next to the name of each file, you will see either 'Incomplete' or 'Complete'.\n"
                "\tNote:'Incomplete' means there is still more data to enter, while 'Complete' means it is ready to be sorted.\n"
                "4.)Once all files you wish to sort are ready and marked as 'Complete,' press the Sort button to sort the files into the target directory.\n"
                "\tNote:if a client directory does not exist, a new one will be created automatically.\n"
                "5.)If any unexpected issues occur, please contact Scott directly or raise an issue on GitHub.\n"
            )
        )
        getting_started_body.grid(row=1, column=0, padx=10, pady=2, sticky='w')

        self.body_labels.append(getting_started_body)

        # --- Data Format Guidelines ------------------------------------------------------------------------
        format_header = ctk.CTkLabel(self.body, text="Valid Data Formats", **style_label_body_header)
        format_header.grid(row=2, column=0, padx=5, pady=(10, 2), sticky='w')

        format_body = ctk.CTkLabel(self.body, **style_label_body,
            text=(
                "- Client Name: First and last name, capitalized \n\t--(e.g., 'John Smith')\n"
                "- Business Name: All caps with optional numbers and spaces \n\t--(e.g., 'ABC 123 LLC')\n"
                "- Year: 4-digit numeric value \n\t--(e.g., 2023)\n"
                "- File Description: Optional. Brief text describing the file’s contents or purpose."
            )
        )
        format_body.grid(row=3, column=0, padx=10, pady=2, sticky='w')

        self.body_labels.append(format_body)

        # --- Miscellaneous Tips ------------------------------------------------------------------------
        tips_header = ctk.CTkLabel(self.body, text="Helpful Tips", **style_label_body_header)
        tips_header.grid(row=4, column=0, padx=5, pady=(10, 2), sticky='w')

        tips_body = ctk.CTkLabel(self.body,  **style_label_body,
            text=(
                "- Double-check client types (Client vs Business) for proper validation.\n"
                "- Use the 'Settings' menu to configure file paths before importing data.\n"
            )
        )
        tips_body.grid(row=5, column=0, padx=10, pady=(2, 10), sticky='w')

        self.body_labels.append(tips_body)

        self.after(100, update_wraplengths)