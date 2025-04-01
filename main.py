from FileSorter.FileSorter_Sorter import Sorter
from FileSorter.FileSorter_DataHandler import DataHandler
from FileSorter.FileSorter_Controller import Controller
from FileSorter.FileSorter_GUI import FileSorter

if __name__ == '__main__':
    dataHandler = DataHandler()
    sorter = Sorter()

    controller = Controller(dataHandler, sorter)

    program = FileSorter(controller)
    program.mainloop()