import sys
from typing import Any
import webbrowser as wb
import pandas as pd
import yaml
import os
import logging

from Utility.constants import (
    FILE_NAME, STATUS, CLIENT_TYPE, CLIENT_NAME, CLIENT_2_NAME, YEAR, DESCRIPTION,
    FILES_ID, TARGET_ID,
    DEFAULT_VALUES, DEFAULT_SETTINGS, DEFAULT_DATAFRAME, FileData)

class DataHandler:
    def __init__(self):
        logging.debug("Init Datahandler")
        self.files_df = DEFAULT_DATAFRAME
        self.init_directories()
        self.olddata_path = self.resource_path(r"PersistentData/Data/olddata.yaml")
        self.settings_path = self.resource_path(r"PersistentData/Data/settings.yaml")
        self.file_path = ""
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
        settings = {
            FILES_ID:self.file_path,
            TARGET_ID:self.target_path
        }

        logging.debug(f"saving settings: {settings} to {self.settings_path}")
        with open(self.settings_path, 'w') as file:
            yaml.dump(settings,
                      stream=file,
                      default_flow_style=False,
                      sort_keys=False)

    def apply_settings(self, settings:dict) -> None:
        def get_valid_path(key: str) -> str:
            path = settings.get(key)
            if not path:
                logging.info(f"{key} is empty, setting to ''")
                return ""
            if not os.path.exists(path):
                logging.info(f"{key} path does not exist, setting to ''")
                return ""
            return path

        self.file_path = get_valid_path(FILES_ID)
        self.target_path = get_valid_path(TARGET_ID)

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
        expected_columns = set(FileData.__annotations__.keys())
        actual_columns = set(self.files_df)

        unexpected = actual_columns - expected_columns
        if unexpected:
            logging.warning(f"unexpected columns in dataframe found: {unexpected}")
            return False

        missing = expected_columns - actual_columns
        if missing:
            logging.warning(f"missing columns in dataframe: {missing}")
            return False

        if not self.files_df[FILE_NAME].is_unique:
            logging.warning(f"duplicate file names found! file names: {self.files_df[FILE_NAME]}")
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
        Removes rows correlating to file names that no longer exist
        """
        logging.debug(f"Checking if path exists: {self.file_path} -> {os.path.exists(self.file_path)}")
        if self.file_path == "" or not os.path.exists(self.file_path):
            logging.warning("dataHandler.filter_data: called with invalid file path")
            self.files_df = DEFAULT_DATAFRAME
            return

        actual_files = list(os.listdir(self.file_path))
        if actual_files and not self.files_df.empty:
            self.files_df = self.files_df.loc[self.files_df[FILE_NAME].isin(actual_files)]
        else:
            self.files_df = DEFAULT_DATAFRAME

    def scan_files(self) -> None:
        """
        Scans file_path for any file names that are not already in the existing dataframe
        if found, populates a new row for each file with default values
        """
        logging.debug(f"Checking if path exists: {self.file_path} -> {os.path.exists(self.file_path)}")
        if self.file_path == "" or not os.path.exists(self.file_path):
            logging.warning("dataHandler.scan_files: called with invalid file path")
            return

        actual_files = os.listdir(self.file_path)
        files_in_df = set(self.files_df['File_Name'])
        for file in actual_files:
            duplicate_file = file in files_in_df
            not_pdf = not file.endswith(".pdf")
            if duplicate_file or not_pdf:
                pass
            else:
                logging.debug(f"new file found {file}, adding with filler data...")
                new_row = pd.DataFrame({
                    'File_Name': [file],
                    'File_Status': DEFAULT_VALUES[STATUS],
                    'Client_Type': DEFAULT_VALUES[CLIENT_TYPE],
                    'Client_Name': DEFAULT_VALUES[CLIENT_NAME],
                    'Client_2_Name': DEFAULT_VALUES[CLIENT_2_NAME],
                    'Year': DEFAULT_VALUES[YEAR],
                    'File_Description': DEFAULT_VALUES[DESCRIPTION]
                })
                self.files_df = pd.concat([self.files_df, new_row], ignore_index=True)

    def update_row(self, file_data: FileData) -> None:
        logging.debug(f"updating row {file_data[FILE_NAME]}...")

        matching = self.files_df.loc[self.files_df[FILE_NAME] == file_data[FILE_NAME]]
        if matching.empty:
            logging.warning(f"no matching row to update: {file_data[FILE_NAME]}")
            return
        row_index = matching.index[0]

        self.files_df.at[row_index, STATUS] = file_data[STATUS]
        self.files_df.at[row_index, CLIENT_TYPE] = file_data[CLIENT_TYPE]
        self.files_df.at[row_index, CLIENT_NAME] = file_data[CLIENT_NAME]
        self.files_df.at[row_index, CLIENT_2_NAME] = file_data[CLIENT_2_NAME]
        self.files_df.at[row_index, YEAR] = int(file_data[YEAR])
        self.files_df.at[row_index, DESCRIPTION] = file_data[DESCRIPTION]

        logging.debug(f"New dataframe: {self.files_df.to_string()}")
        self.save_data_instance()

    def update(self) -> None:
        logging.debug("updating...")
        self.load_data_instance()
        self.filter_data()
        self.scan_files()

    def open_file(self,file_name) -> str:
        if self.file_path == "":
            error = "File path undefined.\nPlease specify a file path in settings."
            logging.warning(error)
            return error
        full_path = os.path.join(self.file_path, file_name)
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
        logging.debug(f"returning copy of df:\n{self.files_df}")
        return self.files_df.copy()

    def get_base_directory(self) -> str:
        logging.debug("returning base directory")
        return self.resource_path("")

    def resource_path(self, relative_path: str) -> str:
        """
        given a relative path (relative to the base directory of the project or exe,
        return the full path
        (e.g. C:/Files/Somewhere/SEK FileSorter/TargetThing given relative_path = SEK FileSorter/TargetThing)
        """
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))) #path to project directory or where the exe is located
        if relative_path == "":
            logging.debug(f"returning base path: {base_path}")
        else:
            logging.debug(f"returning base path: {base_path} merged with relative path: {relative_path}")
        return os.path.join(base_path, relative_path).replace("\\","/")

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

    def get_row(self, file_name: str) -> dict | None:
        row = self.files_df.loc[self.files_df[FILE_NAME] == file_name]
        logging.debug(f"returning row for file: {file_name}")
        if not row.empty:
            return row.iloc[0].apply(lambda x: x.item() if hasattr(x, 'item') else x).to_dict() #cast to pure Python types
        return None