import logging
import re
from typing import List
import pandas as pd
from customtkinter import CTkBaseClass

from Core.Sorter import Sorter
from Core.DataHandler import DataHandler
from Utility.constants import (
    FILE_NAME, STATUS, CLIENT_TYPE, CLIENT_NAME, CLIENT_2_NAME, YEAR, DESCRIPTION,  # indexes
    FILES_ID, TARGET_ID, STATUS_SUCCESS, STATUS_DO_NOTHING,
    NAME_VALIDATORS, VALID_YEAR, DEFAULT_VALUES,
    RowData,
)

class Controller:

    def __init__(self, data_handler:DataHandler | None = None, sorter:Sorter | None = None):
        logging.debug("Init Controller")
        self.data_handler = data_handler or DataHandler()
        self.sorter = sorter or Sorter(target_path=self.data_handler.get_target_path())
        self.observers = []

    #TODO: set observers to UI components
    def new_observer(self, observer: CTkBaseClass) -> None:
        self.observers.append(observer)

    def update(self) -> None:
        self.data_handler.update()
        for observer in self.observers:
            observer.update()

    def get_data_copy(self) -> pd.DataFrame:
        return self.data_handler.get_data_copy()

    def get_row(self, file_path:str) -> RowData:
        return self.data_handler.get_row(file_path)

    def open_file(self, file_path:str) -> str:
        error_msg = self.data_handler.open_file(file_path)
        return error_msg

    def get_path(self, pathID:str) -> str:
        path_map = {
            FILES_ID: self.data_handler.get_file_paths(),
            TARGET_ID: self.data_handler.get_target_path()
        }
        path = path_map.get(pathID)
        if path is None:
            logging.error(f"pathID invalid:{pathID}")
            return ""
        return path

    def set_file_path(self, path:list[str]) -> None:
        self.data_handler.set_file_paths(path)

    def set_target_path(self, path: str) -> None:
        self.data_handler.set_target_path(path)
        self.sorter.set_target_path(path)

    def set_path(self, pathID:str, path:str | list[str]) -> None:
        if path == '':
            logging.warning("called with empty path, no action taken from controller")
            return
        path_setters = {
            FILES_ID: self.set_file_path,
            TARGET_ID: self.set_target_path
        }

        setter = path_setters.get(pathID)
        if setter:
            setter(path)
            self.update()
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

    def sort_files(self) -> str:
        """
        filter_data removes any files that no longer exist
        Retrieve and store every row that has STATUS == True (meaning the file is ready to sort)
        Pass these rows into sorter to be sorted
        Afterward, call filter_data again to filter the now sorted files out of files_df
        Finally, if the sorting was a success, save the current instance of files_df to olddata.yaml
        """
        self.data_handler.filter_data()
        data_copy = self.data_handler.get_data_copy()
        files_ready = data_copy.loc[data_copy[STATUS] == True]
        if files_ready.empty:
            logging.debug("Sort button pressed, but files_ready is empty.")
            return STATUS_DO_NOTHING
        else:
            logging.debug(f"The following files are ready for sorting:\n{files_ready[FILE_NAME].to_string()}")
            message = self.sorter.sort_files(files_ready)
            if message == STATUS_SUCCESS:
                self.data_handler.save_data_instance()
            self.update()
            return message
