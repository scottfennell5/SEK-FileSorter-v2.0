from Sorter import Sorter
from DataHandler import DataHandler
from Controller import Controller
from GUI_Root import FileSorter

if __name__ == '__main__':
    dataHandler = DataHandler()
    sorter = Sorter()

    controller = Controller(dataHandler, sorter)

    program = FileSorter(controller)
    program.mainloop()