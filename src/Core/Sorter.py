import logging
import os
import pandas as pd

from Utility.constants import (
    FILE_NAME, CLIENT_TYPE, CLIENT_NAME, CLIENT_2_NAME, YEAR, DESCRIPTION,
    CLIENT, BUSINESS, INCOME_TAX, STATUS_DO_NOTHING, STATUS_SUCCESS, FILE_PATH)


class Sorter:
    def __init__(self, target_path:str):
        self.target_path = target_path

    def set_target_path(self, path:str) -> None:
        logging.debug(f"set target_path to {path}")
        self.target_path = path

    def get_target_path(self) -> str:
        logging.debug(f"returned target_path: {self.target_path}")
        return self.target_path

    def sort_files(self, files_to_sort:pd.DataFrame) -> str:
        """
        Accepts a pandas dataframe containing all files where STATUS is True, sorts them into directories based on provided info
        Creates a new directory & income tax folder if one is not found
        """
        sorted_files = []
        if not os.path.exists(self.target_path):
            logging.info("sort called without valid target path")
            return "Error: Sorter needs a valid target path. \nPlease select a path in Settings."

        files_to_sort.set_index(FILE_PATH, drop=False)
        files = list(files_to_sort.index)

        for file_path in files:
            row = files_to_sort.loc[file_path]
            file_name = row[FILE_NAME]
            client_type = row[CLIENT_TYPE]

            if not os.path.exists(file_path):
                logging.warning(f"file {file_name} not found at expected location: {file_path}")
                continue

            directory_creator = {
                CLIENT: self.create_client_directory,
                BUSINESS: self.create_business_directory
            }[client_type]
            filename_creator = {
                CLIENT: self.create_client_filename,
                BUSINESS: self.create_business_filename
            }[client_type]

            name = row[CLIENT_NAME]
            name_2 = row[CLIENT_2_NAME]
            directory = directory_creator(name, name_2)
            full_directory = os.path.join(self.target_path, directory, INCOME_TAX)

            os.makedirs(full_directory, exist_ok=True)

            new_filename = filename_creator(row)

            source = file_path
            destination = os.path.join(full_directory, new_filename)

            os.rename(source,destination)
            logging.debug(f"--------------FILE SORTED-----------------\nmoved {file_name}\nfrom: {source}\nto: {destination}")

            sorted_files.append(file_name)

        logging.debug(f"file sorting complete, files sorted: {sorted_files}")
        return STATUS_SUCCESS

    def create_client_directory(self, name:str, name_2:str) -> str:
        first, last = name.split(" ")
        directory_name = f"{last}, {first}"

        if name_2:
            first2, last2 = name_2.split(" ")
            if last2 == last:
                directory_name += f" & {first2}"
            else:
                directory_name += f" & {last2}, {first2}"

        return directory_name

    def create_business_directory(self, name:str, name_2:str) -> str:
        directory_name = name

        if name_2:
            directory_name += f" & {name_2}"

        return directory_name

    def create_client_filename(self, row:pd.Series) -> str:
        last = row[CLIENT_NAME].split(" ")[1]
        year = row[YEAR]
        desc = row[DESCRIPTION]

        return f"{last} {year} {desc}.pdf"

    def create_business_filename(self, row:pd.Series) -> str:
        name = row[CLIENT_NAME][:-4] #remove suffix such as " INC" or " LLC"
        year = row[YEAR]
        desc = row[DESCRIPTION]

        return f"{name} {year} {desc}.pdf"