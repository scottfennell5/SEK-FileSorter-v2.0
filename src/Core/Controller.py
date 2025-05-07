import logging
import re
from typing import List
import pandas as pd

from Core.Sorter import Sorter
from Core.DataHandler import DataHandler
from Utility.constants import (
    FILE_NAME, STATUS, CLIENT_TYPE, CLIENT_NAME, CLIENT_2_NAME, YEAR, DESCRIPTION, #indexes
    FILES_ID, TARGET_ID,
    NAME_VALIDATORS, VALID_YEAR, DEFAULT_VALUES,
    FileData #type hinting
)

class Controller:

    def __init__(self, data_handler:DataHandler|None = None, sorter:Sorter | None = None):
        logging.debug("Init Controller")
        self.data_handler = data_handler or DataHandler()
        self.sorter = sorter or Sorter(file_path=self.data_handler.get_file_path(),
                                       target_path=self.data_handler.get_target_path())
        self.observers = [self.data_handler, self.sorter]

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

    def update(self) -> None:
        for observer in self.observers:
            observer.update()

    def get_data_copy(self) -> pd.DataFrame:
        return self.data_handler.get_data_copy()

    def get_row(self, file_name:str) -> FileData:
        return self.data_handler.get_row(file_name)

    def open_file(self, file_name:str) -> str:
        error_msg = self.data_handler.open_file(file_name)
        return error_msg

    def get_path(self, pathID:str) -> str:
        path_map = {
            FILES_ID: self.data_handler.get_file_path(),
            TARGET_ID: self.data_handler.get_target_path()
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
            TARGET_ID: self.set_observer_targetpath
        }

        setter = path_setters.get(pathID)
        if setter:
            setter(path)
        else:
            logging.error(f"Invalid pathID: {pathID}")

    def save_settings(self) -> None:
        self.data_handler.save_settings()

    def get_resource_path(self, relative_path:str) -> str:
        return self.data_handler.resource_path(relative_path)

    def get_base_directory(self) -> str:
        return self.data_handler.get_base_directory()

    def save_row_changes(self, file_data:dict, radio_value:bool) -> List[str]:
        """
        Given submitted file data in the form of a dictionary, validate and update the row in files_df
        Note that in the case that only some columns pass validation, those valid columns will still be updated in files_df
        radio_value = True if there is a client 2, otherwise False
        """
        logging.debug(f"row changes submitted for {file_data[FILE_NAME]}, validating...")

        valid_data, errors = self.clean_and_validate_row(file_data, radio_value)

        if not errors:
            logging.debug(f"data passed validation!")
        else:
            logging.debug(f"errors: {errors}")
        self.data_handler.update_row(valid_data)
        return errors

    def clean_and_validate_row(self, file_data:dict, client2:bool) -> tuple[dict,List[str]]:
        """
        Given a row and whether client 2 exists or not, check if each value follows the specified regex format in constants
        If a given column does not pass validation, set the column's value back to its default value
        If any columns were not valid, status will be set to False, but if all columns pass, status will be set to True
        Return a tuple that contains the validated row and a list of columns that need fixed
        """
        logging.debug(f"validating row: {file_data}")
        errors = []
        cleaned_data = DEFAULT_VALUES.copy()
        cleaned_data[FILE_NAME] = file_data[FILE_NAME]
        cleaned_data[CLIENT_TYPE] = file_data[CLIENT_TYPE]

        try:
            validator = NAME_VALIDATORS[cleaned_data[CLIENT_TYPE]]
        except KeyError:
            logging.warning(f"invalid client type '{cleaned_data[CLIENT_TYPE]}'")
            return file_data, ["Client Type"]

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
        """
        Retrieve and store every row that has STATUS == True (meaning the file is ready to sort)
        Pass these rows into sorter to be sorted
        Afterward, call filter_data to filter the now sorted files out of files_df
        """
        self.data_handler.filter_data()
        data_copy = self.data_handler.get_data_copy()
        files_ready = data_copy.loc[data_copy[STATUS] == True]
        logging.debug(f"The following files are ready for sorting:\n{files_ready.to_string()}")
        self.sorter.sort_files(files_ready)
        self.data_handler.filter_data()