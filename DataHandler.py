import sys
import pandas as pd
import duckdb as ddb
import yaml
import os
import logging

from yaml.scanner import ScannerError
from yaml.parser import ParserError

from Utility.constants import (
    FILE_NAME, STATUS, CLIENT_TYPE, CLIENT_NAME, CLIENT_NAME_2, YEAR, DESCRIPTION,
    DEFAULT_VALUES)

class DataHandler:

    files_dict = {FILE_NAME:pd.Series(dtype="string"),
                  STATUS:pd.Series(dtype=bool),
                  CLIENT_TYPE:pd.Series(dtype="string"),
                  CLIENT_NAME:pd.Series(dtype="string"),
                  CLIENT_NAME_2:pd.Series(dtype="string"),
                  YEAR:pd.Series(dtype=int),
                  DESCRIPTION:pd.Series(dtype="string")}

    def __init__(self):
        logging.debug("Init Datahandler")
        self.files_df = pd.DataFrame(self.files_dict)
        self.olddata_path = self.resource_path(r"PersistentData/Data/olddata.yaml")
        self.settings_path = self.resource_path(r"PersistentData/Data/settings.yaml")
        self.file_path = ""
        self.target_path = ""
        self.browser_path = ""
        self.load_settings()
        self.update()

    def get_data_copy(self):
        logging.debug(f"returning copy of df:\n{self.files_df}")
        return self.files_df.copy()

    def open_file(self,file_name):
        if self.file_path == "":
            logging.warning("File path undefined! cant open file")
        if file_name in os.listdir(self.file_path):
            #open file
            pass
        else:
            logging.info(f"File {file_name} not found!")
            return False

    def load_settings(self):
        try:
            with open(self.settings_path, 'r') as file:
                settings = yaml.load(file, Loader=yaml.FullLoader)
        except FileNotFoundError:
            settings = {
                "file_path": "",
                "target_path": "",
                "browser_path": ""
            }
            with open(self.settings_path, 'w') as file:
                yaml.dump(settings, file, default_flow_style=False)

        def get_valid_path(key):
            path = settings.get(key)
            if not path:
                logging.info(f"{key} is empty, setting to ''")
                return ""
            return path

        self.file_path = get_valid_path("file_path")
        self.target_path = get_valid_path("target_path")
        self.browser_path = get_valid_path("browser_path")

    def save_settings(self):
        settings = {
            "file_path":self.file_path,
            "target_path":self.target_path,
            "browser_path":self.browser_path
        }

        logging.debug(f"saving settings: {settings} to {self.settings_path}")
        with open(self.settings_path, 'w') as file:
            yaml.dump(settings,
                      stream=file,
                      default_flow_style=False,
                      sort_keys=False)

    def save_data_instance(self):
        with open(self.olddata_path,'w') as file:
            yaml.dump(self.files_df.to_dict(orient="records"),
                      stream=file,
                      default_flow_style=False,
                      sort_keys=False)

    def load_data_instance(self):
        """
        Attempts to read olddata.yaml into a dataframe
        In the event that something goes wrong (file is missing, empty, corrupted, etc.)
        a blank olddata.yaml is created or overwritten in PersistentData/Data.
        """
        try:
            with open(self.olddata_path, 'r') as file:
                self.files_df = pd.json_normalize(yaml.load(file, Loader=yaml.FullLoader))
                return
        except NotImplementedError:
            logging.warning("tried to read empty data file")
        except FileNotFoundError:
            logging.warning("olddata.yaml does not exist")
        except Exception as e:
            logging.warning(f"unexpected error occurred while loading data: {e}")

        self.files_df = pd.DataFrame(self.files_dict)
        with open(self.olddata_path, 'w') as file:
            yaml.dump(self.files_df.to_dict(orient="records"),
                      stream=file,
                      default_flow_style=False,
                      sort_keys=False)
        logging.info("created new empty olddata.yaml")

    def filter_data(self):
        #Removes rows that correlate to files that no longer exist or cannot be found.
        logging.debug(f"Checking if path exists: {self.file_path} -> {os.path.exists(self.file_path)}")
        if self.file_path == "" or not os.path.exists(self.file_path):
            logging.warning("dataHandler.filter_data: called with invalid file path")
            self.files_df = pd.DataFrame(self.files_dict)
            return

        actual_files = list(os.listdir(self.file_path))
        if actual_files and not self.files_df.empty:
            con = ddb.connect()
            con.register("df", self.files_df)
            self.files_df = con.sql(
                query=f"SELECT * FROM df WHERE {FILE_NAME} IN ?",
                params=[actual_files]
            ).df()
        else:
            self.files_df = pd.DataFrame(self.files_dict)

    def scan_files(self):
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
                    'Client_Name_2': DEFAULT_VALUES[CLIENT_NAME_2],
                    'Year': DEFAULT_VALUES[YEAR],
                    'File_Description': DEFAULT_VALUES[DESCRIPTION]
                })
                self.files_df = pd.concat([self.files_df, new_row], ignore_index=True)

    def update(self):
        logging.debug("updating...")
        self.load_data_instance()
        self.filter_data()
        self.scan_files()

    def set_file_path(self, path):
        logging.debug(f"set file_path to {path}")
        self.file_path = path

    def get_file_path(self):
        logging.debug(f"returned file_path: {self.file_path}")
        return self.file_path

    def set_target_path(self, path):
        logging.debug(f"set target_path to {path}")
        self.target_path = path

    def get_target_path(self):
        logging.debug(f"returned target_path: {self.target_path}")
        return self.target_path

    def set_browser_path(self, path):
        logging.debug(f"set browser_path to {path}")
        self.browser_path = path

    def get_browser_path(self):
        logging.debug(f"returned browser_path: {self.browser_path}")
        return self.browser_path

    def get_base_directory(self):
        logging.debug("returning base directory")
        return self.resource_path("")

    def resource_path(self, relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))) #path to project directory or where the exe is located
        logging.debug(f"returning base path: {base_path} merged with relative path: {relative_path}")
        return os.path.join(base_path, relative_path)

    def get_row(self, file_name):
        con = ddb.connect()
        con.register("df", self.files_df)
        row = con.sql(
            query=f"SELECT * FROM df WHERE {FILE_NAME} = ?",
            params=[file_name]
        ).df()

        logging.debug(f"returning row:\n{row}")
        if not row.empty:
            return row.iloc[0].apply(lambda x: x.item() if hasattr(x, 'item') else x).to_dict() #cast to pure Python types
        return None

    def update_row(self, file_data):
        logging.debug(f"updating row {file_data[FILE_NAME]}...")

        matching = self.files_df.loc[self.files_df[FILE_NAME] == file_data[FILE_NAME]]
        if matching.empty:
            logging.warning(f"no matching row to update: {file_data[FILE_NAME]}")
            return
        row_index = matching.index[0]

        self.files_df.loc[row_index, STATUS] = file_data[STATUS]
        self.files_df.loc[row_index, CLIENT_TYPE] = file_data[CLIENT_TYPE]
        self.files_df.loc[row_index, CLIENT_NAME] = file_data[CLIENT_NAME]
        self.files_df.loc[row_index, CLIENT_NAME_2] = file_data[CLIENT_NAME_2]
        self.files_df.loc[row_index, YEAR] = int(file_data[YEAR])
        self.files_df.loc[row_index, DESCRIPTION] = file_data[DESCRIPTION]

        logging.debug(f"New dataframe: {self.files_df.to_string()}")
        self.save_data_instance()

    def remove_row(self, file_name):
        pass