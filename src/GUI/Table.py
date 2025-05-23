import logging
import time
import math
import customtkinter as ctk
from PIL import ImageFont

from Core import Controller
from GUI import Home
from Utility.constants import CLIENT_NAME, DEFAULT_VALUES
from Utility.style import style_status_incomplete, style_label_body, style_button, style_status_complete, style_invisible_frame

class Table(ctk.CTkFrame):
    def __init__(self, master:Home, controller:Controller,
                 row_height=40, visible_rows=14, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.grandparent = master.master
        self.controller = controller
        self.row_height = row_height
        self.visible_rows = visible_rows

        self.current_tab = 1
        self.total_tabs = 1

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.header = ctk.CTkFrame(self, **style_invisible_frame)
        self.header.grid(row=0,column=0,sticky="ns")

        self.body = ctk.CTkFrame(self, **style_invisible_frame)
        self.body.grid(row=1,column=0,sticky="nsew")
        self.body.grid_columnconfigure(0, weight=1)

        self.rows = []
        for i in range(visible_rows):
            label = ctk.CTkLabel(self.body, text="", **style_label_body)
            label.grid(row=i, column=0, padx=(0,8), pady=(0,10), sticky='nwe')
            label_status = ctk.CTkLabel(self.body, corner_radius=5, width=50, justify="left", anchor="w")
            label_status.grid(row=i, column=1, padx=(0,8), pady=(0,10), sticky='nw')
            button = ctk.CTkButton(self.body, text="Open File", width=125, **style_button)
            button.grid(row=i, column=2, sticky='nw')
            self.rows.append((label, label_status, button))

    def populate_header(self) -> None:
        """
        Populate header based on current tab
        <- Current tab: curr/max ->
        """
        for widget in self.header.winfo_children():
            widget.destroy()

        def go_prev() -> None:
            if self.current_tab > 1:
                self.current_tab -= 1
                self.populate_body()
                self.populate_header()

        def go_next() -> None:
            if self.current_tab < self.total_tabs:
                self.current_tab += 1
                self.populate_body()
                self.populate_header()

        prev_button = ctk.CTkButton(self.header, text="⟵", width=30, **style_button,
                                    command=lambda:go_prev(),
                                    state="normal" if self.current_tab > 1 else "disabled")
        prev_button.grid(row=0,column=0, padx=(0,10), pady=(0,10))

        tab_label = ctk.CTkLabel(self.header, text=f"{self.current_tab}  /  {self.total_tabs}", **style_label_body)
        tab_label.grid(row=0,column=1, pady=(0,10))

        next_button = ctk.CTkButton(self.header, text="⟶", width=30, **style_button,
                                    command=lambda:go_next(),
                                    state="normal" if self.current_tab < self.total_tabs else "disabled")
        next_button.grid(row=0,column=2, padx=(10,0), pady=(0,10))

    def populate_body(self, clients:list[tuple[str,str,str,str]]) -> None:
        """
        Populates the body with a set number of rows starting from the current tab index
        up to the max number of visible rows.
        If the number of remaining rows is less than the total
        """
        self.total_tabs = math.ceil(len(clients) / self.visible_rows)
        logging.debug(f"loading table at current tab {self.current_tab}/{self.total_tabs}")

        start = time.time()
        start_index = ((self.current_tab-1) * self.visible_rows)
        for i, (label, label_status, button) in enumerate(self.rows):
            data_index = start_index + i
            if data_index < len(clients):
                file, path, status, name = clients[data_index]
                label_text = name
                if name == DEFAULT_VALUES[CLIENT_NAME]:
                    label_text = file
                label.configure(text=label_text)
                style = style_status_complete if status else style_status_incomplete
                label_status.configure(**style)

                button.configure(command=lambda
                    file_row=self.controller.get_row(path): self.grandparent.open_file(file_row, path))
                label.grid()
                label_status.grid()
                button.grid()
            else:
                label.grid_remove()
                label_status.grid_remove()
                button.grid_remove()
        end = time.time()
        logging.debug(f"populate_body: completed in {round(end - start, 3)}s")

    def truncate_all_names(self) -> None:
        font = ImageFont.truetype("arial.ttf",14)
        for label, label_status, button in self.rows:
            self.update_idletasks()
            available_width = label.winfo_width()
            full_text = label.cget("text")
            text_width = font.getlength(full_text)
            if text_width > available_width:
                truncated = self.truncate_to_fit(full_text, available_width, font)
                label.configure(truncated)

    def truncate_to_fit(self, text, max_width, font) -> str:
        ellipsis = "..."
        while (font.getlength(text+ellipsis) > max_width) and (len(text) > 0):
            text = text[:-1]
        return text+ellipsis if text else ellipsis

    def refresh_values(self, clients:list[tuple[str,str,str,str]]) -> None:
        self.after(100, self.truncate_all_names)
        self.populate_header()
        self.populate_body(clients)
