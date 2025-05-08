import shutil
from datetime import datetime, timedelta
import logging
import os
import sys
from filelock import FileLock
from threading import Thread, Lock

from Core.Controller import Controller
from Core.GUI_Root import FileSorter

def cleanup_logs(log_root:str, days_to_keep:int = 30) -> None:
    cutoff_date = datetime.now() - timedelta(days=days_to_keep)

    for folder in os.listdir(log_root):
        folder_path = os.path.join(log_root, folder)
        if os.path.isdir(folder_path):
            try:
                folder_date = datetime.strptime(folder, "%B %d %Y")
                if folder_date < cutoff_date:
                    shutil.rmtree(folder_path)
            except ValueError:
                continue  # skip folders not matching the date format

def start_logs() -> None:
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    log_root = os.path.join(base_path, "PersistentData", "Logs")

    os.makedirs(log_root, exist_ok=True)
    cleanup_logs(log_root, days_to_keep=30)

    folder_name = datetime.now().strftime("%B %d %Y")
    daily_log_path = os.path.join(log_root, folder_name)
    os.makedirs(daily_log_path, exist_ok=True)

    log_filename = f"{datetime.now():%Y-%m-%d_%H-%M-%S}.txt"
    log_file = os.path.join(daily_log_path, log_filename)

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