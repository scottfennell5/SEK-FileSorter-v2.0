import logging
import os
from typing import List, Callable
import yaml
import pandas as pd

from Utility.constants import (
    FILE_NAME, STATUS, CLIENT_TYPE, CLIENT_NAME, CLIENT_2_NAME, YEAR, DESCRIPTION,
    CLIENT, BUSINESS, INCOME_TAX)


class Sorter:
    def __init__(self, file_path: str, target_path: str):
        self.file_path = file_path
        self.target_path = target_path

    def set_file_path(self, path: str) -> None:
        logging.debug(f"set file_path to {path}")
        self.file_path = path

    def get_file_path(self) -> str:
        logging.debug(f"returned file_path: {self.file_path}")
        return self.file_path

    def set_target_path(self, path: str) -> None:
        logging.debug(f"set target_path to {path}")
        self.target_path = path

    def get_target_path(self) -> str:
        logging.debug(f"returned target_path: {self.target_path}")
        return self.target_path

    def update(self) -> None:
        logging.debug("sorter updated")

    def sort_files(self, files_to_sort: pd.DataFrame) -> tuple[list,list]:
        """
        Accepts a pandas dataframe containing all files where STATUS is True, sorts them into directories based on provided info
        Creates a new directory & income tax folder if one is not found
        Returns: tuple(sorted_files, missing_files)
        """
        sorted_files, missing_files = [], []
        if not os.path.exists(self.file_path):
            logging.info("sort called without valid file path")
            return sorted_files, missing_files
        if not os.path.exists(self.target_path):
            logging.info("sort called without valid target path")
            return sorted_files, missing_files

        files_to_sort.set_index(FILE_NAME, inplace=True)
        files = list(files_to_sort.index)

        for file_name in files:
            row = files_to_sort.loc[file_name]

            file_location = os.path.join(self.file_path,file_name).replace("\\","/")
            if not os.path.exists(file_location):
                logging.warning(f"file {file_name} not found at expected location: {file_location}")
                missing_files.append(file_name)
                continue

            directory_creator = {
                CLIENT: self.create_client_directory,
                BUSINESS: self.create_business_directory
            }[row[CLIENT_TYPE]]
            filename_creator = {
                CLIENT: self.create_client_filename,
                BUSINESS: self.create_business_filename
            }[row[CLIENT_TYPE]]

            name = row[CLIENT_NAME]
            name_2 = row[CLIENT_2_NAME]
            directory = directory_creator(name, name_2)
            full_directory = os.path.join(self.target_path, directory, INCOME_TAX)

            os.makedirs(full_directory, exist_ok=True)

            new_filename = filename_creator(row)

            source = os.path.join(self.file_path, file_name).replace("\\","/")
            destination = os.path.join(full_directory, new_filename).replace("\\","/")

            os.rename(source,destination)
            logging.debug(f"\nmoved {file_name}\nfrom: {source}\nto: {destination}")

            sorted_files.append(file_name)

        print(f"sort: {sorted_files}\nmissing: {missing_files}")
        return sorted_files, missing_files

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

    def create_client_filename(self, row:dict) -> str:
        last = row[CLIENT_NAME].split(" ")[1]
        year = row[YEAR]
        desc = row[DESCRIPTION]

        return f"{last} {year} {desc}.pdf"

    def create_business_filename(self, row:dict) -> str:
        name = row[CLIENT_NAME][:-4]
        year = row[YEAR]
        desc = row[DESCRIPTION]

        return f"{name} {year} {desc}.pdf"
