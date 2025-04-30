from datetime import datetime
import logging
import os
import sys
import yaml

from Controller import Controller
from GUI_Root import FileSorter

def start_logs() -> None:
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    log_path = os.path.join(base_path, "PersistentData\Logs")
    log_name = f"{datetime.now():%Y-%m-%d_%I-%M-%S-%p}.txt"
    log_file = os.path.join(log_path, log_name)

    logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode="w",
                        format=">>[%(asctime)s] [%(levelname)s] [%(filename)s - %(lineno)d - %(funcName)s()]: %(message)s")

if __name__ == '__main__':
    create_logs = True

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