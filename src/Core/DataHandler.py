import sys
import time
from typing import Any
import webbrowser as wb

import pandas
import pandas as pd
import yaml
import os
import logging

from Utility.constants import (
    FILE_NAME, FILE_PATH, STATUS, CLIENT_TYPE, CLIENT_NAME, CLIENT_2_NAME, YEAR, DESCRIPTION,
    FILES_ID, TARGET_ID,
    DEFAULT_VALUES, DEFAULT_SETTINGS, DEFAULT_DATAFRAME, RowData)

class DataHandler:
    def __init__(self):
        logging.debug("Init Datahandler")
        self.files_df = DEFAULT_DATAFRAME
        self.init_directories()
        self.olddata_path = self.resource_path(r"PersistentData/Data/olddata.yaml")
        self.settings_path = self.resource_path(r"PersistentData/Data/settings.yaml")
        self.file_paths = []
        self.target_path = ""
        self.load_settings()
        self.update()

    def init_directories(self):
        """
        Initialize any critical directories before app is run
        """
        full_data_path = os.path.join(self.get_base_directory(),
                                      "PersistentData/Data/")
        os.makedirs(full_data_path, exist_ok=True)

    def load_settings(self) -> None:
        """
        Attempts to load settings into a dictionary from settings.yaml
        if the file is missing, corrupted, or wrong in some way,
        creates a fresh settings.yaml file
        """
        try:
            with open(self.settings_path, 'r') as file:
                settings = yaml.load(file, Loader=yaml.FullLoader)
            if self.validate_settings(settings):
                logging.debug(f"settings loaded successfully: {settings}")
                self.apply_settings(settings)
                return
        except FileNotFoundError:
            logging.warning("settings.yaml not found")
        except Exception as e:
            logging.warning(f"unexpected error reading settings.yaml: {e}")

        logging.info("generating new settings.yaml")
        with open(self.settings_path, 'w') as file:
            yaml.dump(DEFAULT_SETTINGS, file, default_flow_style=False)

    def validate_settings(self, settings:Any) -> bool:
        """
        If settings is a dictionary and contains only the expected settings, returns true
        otherwise, return false
        """
        if not isinstance(settings,dict):
            logging.warning("settings is not a dictionary")
            return False

        actual_keys = set(settings.keys())
        expected_keys = set(DEFAULT_SETTINGS.keys())
        unexpected_keys = actual_keys - expected_keys
        if unexpected_keys:
            logging.warning(f"settings dictionary did not pass validation, unexpected keys: {unexpected_keys}")
            return False
        missing_keys = expected_keys - actual_keys
        if missing_keys:
            logging.warning(f"settings dictionary did not pass validation, missing keys: {missing_keys}")
            return False
        return True

    def save_settings(self) -> None:
        """
        Writes currently stored settings to settings.yaml
        note: will override previously stored settings
        """
        settings = {
            FILES_ID:self.file_paths,
            TARGET_ID:self.target_path
        }

        logging.debug(f"saving settings: {settings} to {self.settings_path}")
        with open(self.settings_path, 'w') as file:
            yaml.dump(settings,
                      stream=file,
                      default_flow_style=False,
                      sort_keys=False)

    def apply_settings(self, settings:dict) -> None:
        def get_valid_path(path: str) -> str | None:
            if not path:
                logging.info(f"Path is empty, setting to ''")
                return None
            if not os.path.exists(path):
                logging.info(f"Path {path} does not exist, setting to ''")
                return None
            return path

        raw_paths = settings.get(FILES_ID, [])
        if not isinstance(raw_paths, list):
            logging.warning(f"Expected a list of paths for {FILES_ID}, got {type(raw_paths).__name__}")
            raw_paths = []

        self.file_paths = [
            validated for path in raw_paths
            if (validated := get_valid_path(path)) is not None
        ]

        print(self.file_paths)

        self.target_path = get_valid_path(settings.get(TARGET_ID, ""))

    def load_data_instance(self) -> None:
        """
        Attempts to read olddata.yaml into a dataframe
        In the event that something goes wrong (file is missing, empty, corrupted, etc.)
        a blank olddata.yaml file is created in PersistentData/Data.
        """
        try:
            with open(self.olddata_path, 'r') as file:
                data = yaml.load(file, Loader=yaml.FullLoader)
                if data is None:
                    logging.info("olddata.yaml is empty, instantiating empty DataFrame for files_df")
                    self.files_df = DEFAULT_DATAFRAME
                    return
                self.files_df = pd.json_normalize(data)
                if self.validate_file_dataframe():
                    return

        except NotImplementedError as e:
            logging.warning(f"tried to read empty data file: {e}")
        except FileNotFoundError:
            logging.warning("olddata.yaml does not exist")
        except Exception as e:
            logging.warning(f"unexpected error occurred while loading data: {e}")

        self.files_df = DEFAULT_DATAFRAME
        with open(self.olddata_path, 'w') as file:
            yaml.dump(self.files_df.to_dict(orient="records"),
                      stream=file,
                      default_flow_style=False,
                      sort_keys=False)
        logging.debug("created new empty olddata.yaml")

    def validate_file_dataframe(self) -> bool:
        """
        Return True if dataframe has exactly the expected columns and unique file names.
        Return False and log warnings if there are unexpected or missing columns,
        or if file names are not unique.
        """
        expected_columns = set(RowData.__annotations__.keys())
        actual_columns = set(self.files_df)

        unexpected = actual_columns - expected_columns
        if unexpected:
            logging.warning(f"unexpected columns in dataframe found: {unexpected}")
            return False

        missing = expected_columns - actual_columns
        if missing:
            logging.warning(f"missing columns in dataframe: {missing}")
            return False

        if self.files_df.duplicated(subset=[FILE_NAME, FILE_PATH]).any():
            logging.warning(f"duplicate file name/path combinations found!")
            return False

        logging.debug("dataframe passed validation")
        return True

    def save_data_instance(self) -> None:
        with open(self.olddata_path,'w') as file:
            yaml.dump(self.files_df.to_dict(orient="records"),
                      stream=file,
                      default_flow_style=False,
                      sort_keys=False)

    def filter_data(self) -> None:
        """
        Removes rows correlating to file names that no longer exist from files_df
        additionally, any paths that no longer exist are removed from file_paths
        """
        verified_df = DEFAULT_DATAFRAME
        existing_paths = []
        for path in self.file_paths:
            logging.debug(f"Checking if path exists: {path} -> {os.path.exists(path)}")
            if os.path.exists(path):
                existing_paths.append(path)
            else:
                logging.warning(f"Path {path} invalid, removing from list")
                continue

            actual_files = list(os.listdir(path))
            if actual_files and not self.files_df.empty:
                path_matches = self.files_df[FILE_PATH] == path
                file_exists = self.files_df[FILE_NAME].isin(actual_files)
                valid_rows = self.files_df.loc[path_matches & file_exists]
                verified_df = pd.concat([verified_df, valid_rows], ignore_index=True)

        self.files_df = verified_df
        self.file_paths = existing_paths

    def scan_files(self) -> None:
        """
        Scans file_path for any file names that are not already in the existing dataframe
        if found, populates a new row for each file with default values
        """
        new_rows = []
        for path in self.file_paths:
            actual_files = os.listdir(path)
            df_file_path_pairs = set(zip(self.files_df['File_Name'], self.files_df['File_Path']))
            for file in actual_files:
                duplicate_file = (file, path) in df_file_path_pairs
                is_pdf = file.endswith(".pdf")
                if not duplicate_file and is_pdf:
                    logging.debug(f"new file found {file}, adding with filler data...")
                    new_row = {
                        FILE_NAME:file,
                        FILE_PATH:path,
                        STATUS:DEFAULT_VALUES[STATUS],
                        CLIENT_TYPE:DEFAULT_VALUES[CLIENT_TYPE],
                        CLIENT_NAME: DEFAULT_VALUES[CLIENT_NAME],
                        CLIENT_2_NAME: DEFAULT_VALUES[CLIENT_2_NAME],
                        YEAR: DEFAULT_VALUES[YEAR],
                        DESCRIPTION: DEFAULT_VALUES[DESCRIPTION],
                    }
                    new_rows.append(new_row)

        if new_rows:
            new_rows_df = pd.DataFrame(new_rows)
            self.files_df = pd.concat([self.files_df,new_rows_df], ignore_index=True)

    def update_row(self, row_data: RowData) -> None:
        """
        Given a row of data for a specific file, file_data, replaces the currently stored information with the
        information given in file_data
        """
        logging.debug(f"updating row {row_data[FILE_NAME]}...")

        name_match = self.files_df[FILE_NAME] == row_data[FILE_NAME]
        path_match = self.files_df[FILE_PATH] == row_data[FILE_PATH]
        matching = self.files_df.loc[name_match & path_match]
        if matching.empty:
            logging.warning(f"no matching row to update: {row_data[FILE_NAME]}")
            return
        if len(matching) > 1:
            logging.warning(
                f"Multiple rows matched (should be impossible): {row_data[FILE_NAME]} at path {row_data[FILE_PATH]}")
        row_index = matching.index[0]

        self.files_df.at[row_index, STATUS] = row_data[STATUS]
        self.files_df.at[row_index, CLIENT_TYPE] = row_data[CLIENT_TYPE]
        self.files_df.at[row_index, CLIENT_NAME] = row_data[CLIENT_NAME]
        self.files_df.at[row_index, CLIENT_2_NAME] = row_data[CLIENT_2_NAME]
        self.files_df.at[row_index, YEAR] = int(row_data[YEAR])
        self.files_df.at[row_index, DESCRIPTION] = row_data[DESCRIPTION]

        logging.debug(f"New row values: {self.files_df.loc[row_index]}")
        self.save_data_instance()

    def update(self) -> None:
        logging.debug("updating...")
        self.load_data_instance()
        self.filter_data()
        self.scan_files()
        logging.debug(f"dataframe updated, new values:\n{self.files_df.to_string()}")

    def open_file(self, file_name:str, file_path:str) -> str:
        """
        Given a file name, attempts to open that file using the default browser specified in the user's windows settings
        If there are no errors, returns an empty string, otherwise logs and returns the specific error as a string
        """
        full_path = os.path.join(file_path, file_name)
        if os.path.exists(full_path):
            new = 2 #open in new tab
            try:
                wb.open(f"file://{full_path}", new=new)
                return ""
            except wb.Error as e:
                logging.warning(f"failed to open with browser: {e}")
                return "Failed to open with default browser,\nPlease check your computer's default browser settings."
        else:
            error = f"File {file_name} not found!"
            logging.info(error)
            return error

    def get_data_copy(self) -> pd.DataFrame:
        return self.files_df.copy()

    def get_base_directory(self) -> str:
        logging.debug("returning base directory")
        return self.resource_path("")

    def resource_path(self, relative_path: str) -> str:
        """
        given a relative path (relative to the base directory of the project or exe),
        return the full path
        (e.g. C:/Files/Somewhere/SEK-FileSorter/TargetThing given relative_path = SEK-FileSorter/TargetThing)
        """
        if hasattr(sys, '_MEIPASS'):
            # Running in PyInstaller bundle
            base_path = sys._MEIPASS
            path = os.path.join(base_path, relative_path)
        else:
            # Running in dev mode
            base_path = os.path.dirname(os.path.abspath(__file__))
            path = os.path.abspath(os.path.join(base_path, "..", relative_path))

        #for consistent formatting
        base_path = base_path.replace("\\","/")
        path = path.replace("\\","/")

        if relative_path == "":
            logging.debug(f"returning base path: '{base_path}'")
        else:
            logging.debug(f"returning base path: '{base_path}' merged with relative path: '{relative_path}' as a full path: '{path}'")
        return path

    def set_file_paths(self, paths: list[str]) -> None:
        logging.debug(f"set file_paths to {paths}")
        self.file_paths = paths

    def get_file_paths(self) -> list[str]:
        return self.file_paths

    def set_target_path(self, path: str) -> None:
        logging.debug(f"set target_path to {path}")
        self.target_path = path

    def get_target_path(self) -> str:
        return self.target_path

    def get_row(self, file_name: str, file_path: str) -> dict | None:
        """
        Given a file name & path, return the row of data that file name correlates to
        Also, cast all column data types to their equivalent Python data types, to avoid NumPy issues
        """

        name_match = self.files_df[FILE_NAME] == file_name
        path_match = self.files_df[FILE_PATH] == file_path
        row = self.files_df.loc[name_match & path_match]
        if not row.empty:
            return row.iloc[0].apply(lambda x: x.item() if hasattr(x, 'item') else x).to_dict()
        return None