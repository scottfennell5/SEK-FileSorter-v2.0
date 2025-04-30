import logging
from typing import List
import yaml
import pandas as pd

from Utility.constants import FILE_NAME, STATUS, CLIENT_TYPE, CLIENT_NAME, CLIENT_2_NAME, YEAR, DESCRIPTION

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

    def sort_files(self, files: pd.DataFrame) -> List[str]:
        """
        Accepts a pandas dataframe containing all files where STATUS is True, sorts them into directories based on provided info
        If the directory is not found, and there is a similar directory (90% match), prompts the user to merge directories
        If yes, renames directory if it is different from the expected name, then moves file
        If no, creates new directory and moves file
        """
        print(files.to_string())
        sorted_files = []
        """
        1.)check if file path exists, check if target path exists
        if either of these conditions fail, abort
        2.)compile a 2d list consisting of the file name, and target directory
        example: [file001.pdf, "Smith, Amanda"] where the client is Amanda Smith in file001.pdf
        3.)for each file:
            1.)check if target directory already exists
            yes: insert file add to list
            no: step 2
            2.)check if any directories exist that are 95% similar to target directory
            if yes:
                I.)prompt user to manually check before merging
                II.)if user authorizes, rename directory to target directory name
                III.)move file to destination in directory
                if no authorization, pass to next file BUT keep file in list
            if no:
                I.)create new directory
                II.)move file to new directory
        """
        return sorted_files

    def create_client_directory(self, row: dict):
        pass

    def create_business_directory(self, row: dict):
        pass

