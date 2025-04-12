import yaml

FILE_NAME = 0
STATUS = 1
CLIENT_TYPE = 2
CLIENT_NAME = 3
CLIENT_NAME_2 = 4
YEAR = 5
DESCRIPTION = 6

class Sorter:
    def __init__(self):
        self.target_path = None

    def update_target_path(self, path):
        self.target_path=path

    def sort_file(self, file_info):
        #file_info = [file name, status, client type, client name, 2nd client name (or None), year, description]
        pass