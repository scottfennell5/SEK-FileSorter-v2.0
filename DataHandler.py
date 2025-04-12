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

    def __init__(self):
        logging.debug("Init Datahandler")
        self.files_df = pd.DataFrame(self.files_dict)
        self.olddata_path = self.resource_path(r"PersistentData\Data\olddata.yaml")
        self.settings_path = self.resource_path(r"PersistentData\Data\settings.yaml")
        self.file_path = ""
        self.target_path = ""

    def get_data_copy(self):
        return self.files_df.copy()

    def load_settings(self):
        with open(self.settings_path, 'r') as file:
            settings = yaml.load(file, Loader=yaml.FullLoader)

        self.file_path = settings["file_path"]
        if (self.file_path is None) or (not os.path.exists(self.file_path)):
            logging.info("dataHandler.load_settings: file_path invalid, setting to empty ''")
            self.file_path = ""

        self.target_path = settings["target_path"]
        if (self.target_path is None) or (not os.path.exists(self.target_path)):
            logging.info("dataHandler.load_settings: target_path invalid, setting to empty ''")
            self.target_path = ""

    def save_settings(self):
        settings = {
            "file_path":self.file_path,
            "target_path":self.target_path
        }

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
        with open(self.olddata_path, 'r') as file:
            self.files_df = pd.json_normalize(yaml.load(file, Loader=yaml.FullLoader))

    def filter_data(self):
        #Removes rows that correlate to files that no longer exist or cannot be found.
        if self.file_path == "":
            logging.warning("dataHandler.filter_data: called with empty file path")
            self.files_df = pd.DataFrame(self.files_dict)
            return

        actual_files = set(os.listdir(self.file_path))
        self.files_df = (self.files_df[self.files_df["File_Name"].isin(actual_files)].reset_index(drop=True))

    def scan_files(self):
        if self.file_path == "":
            logging.warning("dataHandler.scan_files: called with empty file path")
            return

        actual_files = os.listdir(self.file_path)
        files_in_df = set(self.files_df['File_Name'])
        for file in actual_files:
            if file in files_in_df:
                pass #avoids duplicate data
            elif not file.endswith(".pdf"):
                pass #only pdfs are accepted
            else:
                new_row = pd.DataFrame({
                    'File_Name': [file],
                    'File_Status': [False],
                    'Client_Type': ['Client'],
                    'First_Name': ['unknown client'],
                    'Second_Name': [None],
                    'Year': [1984],
                    'File_Description': ['unknown']
                })
                self.files_df = pd.concat([self.files_df, new_row], ignore_index=True)

    def refresh_data(self):
        self.load_data_instance()
        self.filter_data()
        self.scan_files()

    def set_file_path(self, path):
        self.file_path = path

    def get_file_path(self):
        return self.file_path

    def set_target_path(self, path):
        self.target_path = path

    def get_target_path(self):
        return self.target_path

    def get_base_directory(self):
        return self.resource_path("")

    def resource_path(self, relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))) #path to project directory AKA where the exe is located
        return os.path.join(base_path, relative_path)

    def get_row(self, file_name):
        row = self.files_df[self.files_df["File_Name"]==file_name]
        if not row.empty:
            #returns the row as a list, lambda casts the entire row into pure Python types (to avoid NumPy issues)
            return row.iloc[0].apply(lambda x: x.item() if hasattr(x, 'item') else x).tolist()
        return None

    def remove_row(self, file_name):
        pass #remove row from dataframe, if it has been sorted


    def populate_temp_data(self):
        for i in range(1, 30):
            if i == 5:
                new_row = pd.DataFrame({
                    'File_Name': [f'file{i}_andareallylongname.pdf'],
                    'File_Status': [True],
                    'Client_Type': ['Business'],
                    'First_Name': ['REEEEEEEEALLY LONG BUSINESS LLC'],
                    'Second_Name': [None],
                    'Year': [1984],
                    'File_Description': ['unknown']
                })
            elif i == 10:
                new_row = pd.DataFrame({
                    'File_Name': [f'file{i}.pdf'],
                    'File_Status': [True],
                    'Client_Type': ['Person'],
                    'First_Name': ['Josephus Smithington'],
                    'Second_Name': [None],
                    'Year': [1984],
                    'File_Description': ['unknown']
                })
            else:
                new_row = pd.DataFrame({
                    'File_Name': [f'file{i}.pdf'],
                    'File_Status': [False],
                    'Client_Type': ['unknown'],
                    'First_Name': ['unknown client'],
                    'Second_Name': [None],
                    'Year': [1984],
                    'File_Description': ['unknown']
                })
            self.files_df = pd.concat([self.files_df, new_row], ignore_index=True)
        print(self.files_df)