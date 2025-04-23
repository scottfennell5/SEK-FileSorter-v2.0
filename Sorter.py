import logging
import yaml

FILE_NAME = 0
STATUS = 1
CLIENT_TYPE = 2
CLIENT_NAME = 3
CLIENT_NAME_2 = 4
YEAR = 5
DESCRIPTION = 6

class Sorter:
    def __init__(self, file_path, target_path):
        self.file_path = file_path
        self.target_path = target_path

    def set_file_path(self, path):
        self.file_path = path

    def get_file_path(self):
        return self.file_path

    def set_target_path(self, path):
        self.target_path = path

    def get_target_path(self):
        return self.target_path

    def update(self):
        logging.debug("sorter updated (this function does nothing :P)")

    def sort_file(self, file_info):
        #file_info = [file name, status, client type, client name, 2nd client name (or None), year, description]
        pass