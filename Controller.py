import logging

class Controller:

    FILES_ID = "files"
    TARGET_ID = "target"
    BROWSER_ID = "browser"

    def __init__(self, dataHandler, sorter):
        logging.debug("Init Controller")
        self.dataHandler = dataHandler
        self.dataHandler.load_settings()
        self.dataHandler.refresh_data()
        self.sorter = sorter
        self.sorter.update_target_path(self.dataHandler.get_target_path())
        self.observer = None

    def new_observer(self, observer):
        self.observer = observer

    def notify_observer(self):
        self.observer.update()

    def create_logs(self):
        pass #logs when application closes

    def get_data_copy(self):
        return self.dataHandler.get_data_copy()

    def get_row(self, file_name):
        return self.dataHandler.get_row(file_name)

    def open_file(self, file_name):
        self.dataHandler.open_file(file_name)

    def get_path(self, pathID):
        match pathID:
            case self.FILES_ID:
                path = self.dataHandler.get_file_path()
            case self.TARGET_ID:
                path = self.dataHandler.get_target_path()
            case self.BROWSER_ID:
                path = self.dataHandler.get_browser_path()
            case _:
                logging.exception(f"pathID invalid:{pathID}")
                raise ValueError("Invalid pathID passed into controller.get_path()")

        if path is None:
            return ""
        else:
            return path

    def set_path(self, pathID, path):
        if path == '':
            logging.warning("called with empty path, no action taken from controller")
            return
        match pathID:
            case self.FILES_ID:
                self.dataHandler.set_file_path(path)
                self.dataHandler.refresh_data()
            case self.TARGET_ID:
                self.dataHandler.set_target_path(path)
                self.sorter.update_target_path(path)

    def update_files(self):
        self.notify_observer()

    def save_data(self):
        self.dataHandler.save_data_instance()

    def load_data(self):
        self.dataHandler.load_data_instance()

    def check_data(self):
        print(self.dataHandler.get_data_copy())

    def filter_data(self):
        self.dataHandler.filter_data()

    def save_settings(self):
        self.dataHandler.save_settings()

    def get_settings(self):
        self.dataHandler.load_settings()

    def get_resource(self, relative_path):
        return self.dataHandler.resource_path(relative_path)

    def get_base_directory(self):
        return self.dataHandler.get_base_directory()