import logging
import re
import duckdb as ddb

from Sorter import Sorter
from DataHandler import DataHandler
from Utility.constants import (
    FILE_NAME, STATUS, CLIENT_TYPE, CLIENT_NAME, CLIENT_NAME_2, YEAR, DESCRIPTION,
    FILES_ID, TARGET_ID, BROWSER_ID,
    CLIENT, BUSINESS, VALID_NAME_CLIENT, VALID_NAME_BUSINESS, VALID_YEAR, DEFAULT_VALUES)

class Controller:

    def __init__(self):
        logging.debug("Init Controller")
        self.dataHandler = DataHandler()
        self.sorter = Sorter(file_path=self.dataHandler.get_file_path(),
                             target_path=self.dataHandler.get_target_path())
        self.observers = [self.dataHandler, self.sorter]

    def new_observer(self, observer):
        self.observers.append(observer)

    def set_observer_filepath(self, path):
        logging.debug(f"Setting file path to {path} for all observers")
        for observer in self.observers:
            logging.debug(f"observer:{observer} to file path:{path}")
            observer.set_file_path(path)
            observer.update()

    def set_observer_targetpath(self, path):
        logging.debug(f"Setting target path to {path} for all observers")
        for observer in self.observers:
            logging.debug(f"observer:{observer} to target path:{path}")
            observer.set_target_path(path)
            observer.update()

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
            case _ if pathID == FILES_ID:
                path = self.dataHandler.get_file_path()
            case _ if pathID == TARGET_ID:
                path = self.dataHandler.get_target_path()
            case _ if pathID == BROWSER_ID:
                path = self.dataHandler.get_browser_path()
            case _:
                logging.error(f"pathID invalid:{pathID}")
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
            case _ if pathID == FILES_ID:
                self.set_observer_filepath(path)
            case _ if pathID == TARGET_ID:
                self.set_observer_targetpath(path)
            case _ if pathID == BROWSER_ID:
                self.dataHandler.set_browser_path(path)

    def save_settings(self):
        self.dataHandler.save_settings()

    def get_resource(self, relative_path):
        return self.dataHandler.resource_path(relative_path)

    def get_base_directory(self):
        return self.dataHandler.get_base_directory()

    def save_row_changes(self, file_data, radio_value):
        logging.debug(f"row changes submitted for {file_data[FILE_NAME]}, validating...")

        valid_data, errors = self.clean_and_validate_row(file_data, radio_value)

        if not errors:
            logging.debug(f"data passed validation!")
        else:
            logging.debug(f"errors: {errors}")
        self.dataHandler.update_row(valid_data)
        return errors

    def clean_and_validate_row(self, file_data, client2):
        logging.debug(f"validating row: {file_data}")
        errors = []
        cleaned_data = DEFAULT_VALUES.copy()
        cleaned_data[FILE_NAME] = file_data[FILE_NAME]
        cleaned_data[CLIENT_TYPE] = file_data[CLIENT_TYPE]

        name_validators = {
            CLIENT: VALID_NAME_CLIENT,
            BUSINESS: VALID_NAME_BUSINESS
        }
        validator = name_validators[cleaned_data[CLIENT_TYPE]]

        name = file_data[CLIENT_NAME]
        name2 = file_data[CLIENT_NAME_2]

        if re.fullmatch(validator, name):
            cleaned_data[CLIENT_NAME] = name
        else:
            errors.append("Client 1")

        client2_exists = client2 == 1
        if client2_exists:
            if re.fullmatch(validator, name2):
                cleaned_data[CLIENT_NAME_2] = name2
            else:
                errors.append("Client 2")

        year = file_data[YEAR]
        if re.fullmatch(VALID_YEAR, year):
            cleaned_data[YEAR] = year
        else:
            errors.append("Year")

        desc = file_data[DESCRIPTION].strip()
        if desc != "":
            cleaned_data[DESCRIPTION] = desc
        else:
            errors.append("Description")

        cleaned_data[STATUS] = not errors
        return cleaned_data, errors

    def sort_files(self):
        data_copy = self.dataHandler.get_data_copy()
        files_ready = ddb.query(f"SELECT * FROM data_copy WHERE {STATUS}==True").df()
        logging.debug(f"The following files are ready for sorting:\n{files_ready.to_string()}")
        self.sorter.sort_file(files_ready)

    #temp functions
    def save_data(self):
        self.dataHandler.save_data_instance()

    def load_data(self):
        self.dataHandler.load_data_instance()

    def check_data(self):
        print(self.dataHandler.get_data_copy())

    def filter_data(self):
        self.dataHandler.filter_data()

    def get_settings(self):
        self.dataHandler.load_settings()