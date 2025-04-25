import sys
import pandas as pd
import yaml
import os
import logging

class DataHandler:

    files_dict = {'File_Name':pd.Series(dtype="string"),
                  'File_Status':pd.Series(dtype=bool),
                  'Client_Type':pd.Series(dtype="string"),
                  'First_Name':pd.Series(dtype="string"),
                  'Second_Name':pd.Series(dtype="string"),
                  'Year':pd.Series(dtype=int),
                  'File_Description':pd.Series(dtype="string")}

    """
    Defaults:
    'File_Name': [file],
    'File_Status': [False]
    'Client_Type': ['unknown']
    'First_Name': ['unknown client']
    'Second_Name': [None]
    'Year': [-1]
    'File_Description': [None]
    """

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
        return self.files_df.copy()

    def open_file(self,file_name):
        if self.file_path == "":
            logging.warning("File path undefined! cant open file")
        if file_name.isin(os.listdir(self.file_path)):
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

            self.load_settings()

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
        try:
            with open(self.olddata_path, 'r') as file:
                self.files_df = pd.json_normalize(yaml.load(file, Loader=yaml.FullLoader))
        except NotImplementedError:
            logging.warning("tried to read empty data file")
            self.files_df = pd.DataFrame(self.files_dict)
        except FileNotFoundError:
            logging.warning("olddata.yaml does not exist, creating new file")
            with open(self.olddata_path, 'w') as file:
                pass
            self.files_df = pd.DataFrame(self.files_dict)

    def filter_data(self):
        #Removes rows that correlate to files that no longer exist or cannot be found.
        logging.debug(f"Checking if path exists: {self.file_path} -> {os.path.exists(self.file_path)}")
        if self.file_path == "" or not os.path.exists(self.file_path):
            logging.warning("dataHandler.filter_data: called with invalid file path")
            self.files_df = pd.DataFrame(self.files_dict)
            return

        actual_files = set(os.listdir(self.file_path))
        self.files_df = (self.files_df[self.files_df["File_Name"].isin(actual_files)].reset_index(drop=True))

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
                new_row = pd.DataFrame({
                    'File_Name': [file],
                    'File_Status': [False],
                    'Client_Type': ['unknown'],
                    'First_Name': ['unknown client'],
                    'Second_Name': [None],
                    'Year': [-1],
                    'File_Description': [None]
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
        row = self.files_df[self.files_df["File_Name"]==file_name]
        logging.debug(f"returning row: {row}")
        if not row.empty:
            #returns the row as a list, lambda casts the entire row into pure Python types (to avoid NumPy issues)
            return row.iloc[0].apply(lambda x: x.item() if hasattr(x, 'item') else x).tolist()
        return None

    def remove_row(self, file_name):
        pass #remove row from dataframe, if it has been sorted