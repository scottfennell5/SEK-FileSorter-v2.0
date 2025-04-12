from Sorter import Sorter
from DataHandler import DataHandler
from Controller import Controller
from GUI_Root import FileSorter

from datetime import datetime
import logging
from os import path

if __name__ == '__main__':
    dataHandler = DataHandler()
    sorter = Sorter()

    controller = Controller(dataHandler, sorter)

    program = FileSorter(controller)

    log_path = controller.get_resource("PersistentData\Logs")
    now = datetime.now()
    log_name = now.strftime("%m-%d-%Y_%H-%M-%S_log.txt")
    log_file = path.join(log_path,log_name)

    logging.basicConfig(level=logging.INFO, filename=log_file, filemode="w",
                        format="%(asctime)s - %(levelname)s - %(message)s")

    print(log_file)

    program.mainloop()