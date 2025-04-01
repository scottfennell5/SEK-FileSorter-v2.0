import customtkinter as ctk
from customtkinter import CTkScrollableFrame
from functools import partial

from FileSorter_Sorter import Sorter
from FileSorter_DataHandler import DataHandler
from FileSorter_Controller import Controller
from FileSorter_GUI import FileSorter

if __name__ == '__main__':
    dataHandler = DataHandler()
    sorter = Sorter()

    controller = Controller(dataHandler, sorter)

    program = FileSorter(controller)
    program.mainloop()