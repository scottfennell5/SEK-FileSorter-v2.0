from Utility.constants import FILE_NAME, STATUS, CLIENT_TYPE, CLIENT_NAME, CLIENT_NAME_2, YEAR, DESCRIPTION

import logging
import yaml

class Sorter:
    def __init__(self, file_path, target_path):
        self.file_path = file_path
        self.target_path = target_path

    def set_file_path(self, path):
        logging.debug(f"set file_path to {path}")
        self.file_path = path

    def get_file_path(self):
        logging.debug(f"returned file_path: {self.file_path}")
        return self.file_path

    def set_target_path(self, path):
        logging.debug(f"set target_path to {path}")
        self.target_path = path

    def get_target_path(self):
        logging.debug(f"returned target_path: {self.target_path}")
        return self.target_path

    def update(self):
        logging.debug("sorter updated (this function does nothing :P)")

    def sort_file(self, file_info):
        #file_info = [file name, status, client type, client name, 2nd client name (or None), year, description]
        pass