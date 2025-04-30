import logging
import re
from typing import List
import pandas as pd

from Sorter import Sorter
from DataHandler import DataHandler
from Utility.constants import (
    FILE_NAME, STATUS, CLIENT_TYPE, CLIENT_NAME, CLIENT_2_NAME, YEAR, DESCRIPTION, #indexes
    FILES_ID, TARGET_ID, BROWSER_ID,
    NAME_VALIDATORS, VALID_YEAR, DEFAULT_VALUES,
    FileData #type hinting
)

class Controller:

    def __init__(self):
        logging.debug("Init Controller")
        self.dataHandler = DataHandler()
        self.sorter = Sorter(file_path=self.dataHandler.get_file_path(),
                             target_path=self.dataHandler.get_target_path())
        self.observers = [self.dataHandler, self.sorter]

    def new_observer(self, observer: DataHandler | Sorter) -> None:
        self.observers.append(observer)

    def set_observer_filepath(self, path:str) -> None:
        for observer in self.observers:
            observer.set_file_path(path)
            observer.update()

    def set_observer_targetpath(self, path:str) -> None:
        for observer in self.observers:
            observer.set_target_path(path)
            observer.update()

    def get_data_copy(self) -> pd.DataFrame:
        return self.dataHandler.get_data_copy()

    def get_row(self, file_name:str) -> FileData:
        return self.dataHandler.get_row(file_name)

    def open_file(self, file_name:str) -> None:
        self.dataHandler.open_file(file_name)

    def get_path(self, pathID:str) -> str:
        path_map = {
            FILES_ID: self.dataHandler.get_file_path(),
            TARGET_ID: self.dataHandler.get_target_path(),
            BROWSER_ID: self.dataHandler.get_browser_path()
        }
        path = path_map.get(pathID)
        if path is None:
            logging.error(f"pathID invalid:{pathID}")
            return ""
        return path

    def set_path(self, pathID:str, path:str) -> None:
        if path == '':
            logging.warning("called with empty path, no action taken from controller")
            return
        path_setters = {
            FILES_ID: self.set_observer_filepath,
            TARGET_ID: self.set_observer_targetpath,
            BROWSER_ID: self.dataHandler.set_browser_path
        }

        setter = path_setters.get(pathID)
        if setter:
            setter(path)
        else:
            logging.error(f"Invalid pathID: {pathID}")

    def save_settings(self) -> None:
        self.dataHandler.save_settings()

    def get_resource_path(self, relative_path) -> str:
        return self.dataHandler.resource_path(relative_path)

    def get_base_directory(self) -> str:
        return self.dataHandler.get_base_directory()

    def save_row_changes(self, file_data: dict, radio_value: bool) -> List[str]:
        logging.debug(f"row changes submitted for {file_data[FILE_NAME]}, validating...")

        valid_data, errors = self.clean_and_validate_row(file_data, radio_value)

        if not errors:
            logging.debug(f"data passed validation!")
        else:
            logging.debug(f"errors: {errors}")
        self.dataHandler.update_row(valid_data)
        return errors

    def clean_and_validate_row(self, file_data: dict, client2:bool) -> tuple[dict,List[str]]:
        logging.debug(f"validating row: {file_data}")
        errors = []
        cleaned_data = DEFAULT_VALUES.copy()
        cleaned_data[FILE_NAME] = file_data[FILE_NAME]
        cleaned_data[CLIENT_TYPE] = file_data[CLIENT_TYPE]

        validator = NAME_VALIDATORS[cleaned_data[CLIENT_TYPE]]

        name = file_data[CLIENT_NAME]
        name2 = file_data[CLIENT_2_NAME]

        if re.fullmatch(validator, name):
            cleaned_data[CLIENT_NAME] = name
        else:
            errors.append("Client 1")

        client2_exists = client2 == 1
        if client2_exists:
            if re.fullmatch(validator, name2):
                cleaned_data[CLIENT_2_NAME] = name2
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

    def sort_files(self) -> None:
        data_copy = self.dataHandler.get_data_copy()
        files_ready = data_copy.loc[data_copy[STATUS] == True]
        logging.debug(f"The following files are ready for sorting:\n{files_ready.to_string()}")
        remaining_files = self.sorter.sort_files(files_ready)
        raise NotImplementedError

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