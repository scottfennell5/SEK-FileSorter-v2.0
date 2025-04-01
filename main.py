from FileSorter.Sorter import Sorter
from FileSorter.DataHandler import DataHandler
from FileSorter.Controller import Controller
from FileSorter.GUI_Root import FileSorter

if __name__ == '__main__':
    dataHandler = DataHandler()
    sorter = Sorter()

    controller = Controller(dataHandler, sorter)

    program = FileSorter(controller)
    program.mainloop()