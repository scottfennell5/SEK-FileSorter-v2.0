from Controller import Controller
from GUI_Root import FileSorter

from datetime import datetime
import logging
import os
import sys
import yaml

if __name__ == '__main__':

    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    settings_path = os.path.join(base_path, "PersistentData\Data\settings.yaml")
    with open(settings_path, 'r') as file:
        settings = yaml.load(file, Loader=yaml.FullLoader)

    log_path = settings.get("logs_path")
    now = datetime.now()
    log_name = now.strftime("%m-%d-%Y_%H-%M-%S_log.txt")
    log_file = os.path.join(log_path, log_name)

    logging.basicConfig(level=logging.DEBUG, filename=log_file, filemode="w",
                        format="%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s() - %(message)s")

    controller = Controller()

    program = FileSorter(controller)

    try:
        program.mainloop()
    except KeyboardInterrupt as e:
        logging.warning(f"Keyboard interrupt: {e}")
    except Exception as e:
        logging.fatal(f"FATAL ERROR: {e}", exc_info=True)