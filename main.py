from Controller import Controller
from GUI_Root import FileSorter

from datetime import datetime
import logging
import os
import sys
import yaml

def start_logs():
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    config = os.path.join(base_path, "PersistentData\Data\DO_NOT_EDIT.yaml")
    with open(config, 'r') as file:
        logs_path = yaml.load(file, Loader=yaml.FullLoader)

    log_path = logs_path.get("logs_path")
    now = datetime.now()
    log_name = now.strftime("%m-%d-%Y_%H-%M-%S_log.txt")
    log_file = os.path.join(log_path, log_name)

    logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode="w",
                        format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s")

if __name__ == '__main__':
    create_logs = False

    if create_logs:
        start_logs()

    controller = Controller()

    program = FileSorter(controller)

    try:
        program.mainloop()
    except KeyboardInterrupt as e:
        logging.warning(f"Keyboard interrupt: {e}")
    except Exception as e:
        logging.fatal(f"Fatal Error: {e}\nProgram terminated.", exc_info=True)