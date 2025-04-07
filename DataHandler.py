import sys
import pandas as pd
import yaml
import os

class DataHandler:

    files_dict = {'File_Name':pd.Series(dtype="string"),
                  'File_Status':pd.Series(dtype=bool),
                  'Client_Type':pd.Series(dtype="string"),
                  'First_Name':pd.Series(dtype="string"),
                  'Second_Name':pd.Series(dtype="string"),
                  'Year':pd.Series(dtype=int),
                  'File_Description':pd.Series(dtype="string")}
    files_df = pd.DataFrame(files_dict)

    def __init__(self):
        self.olddata_path = self.resourcePath(r"PersistentData\Data\olddata.yaml")
        self.settings_path = self.resourcePath(r"PersistentData\Data\settings.yaml")
        self.file_path = self.resourcePath(r"Files")
        print("init datahandler complete")

    def scanFiles(self):
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

    def getDataCopy(self):
        if self.files_df is None:
            return None
        else:
            return self.files_df.copy()

    def readSettings(self):
        pass

    def saveSettings(self):
        pass

    def saveDataInstance(self):
        with open(self.olddata_path,'w') as file:
            cfg = yaml.dump(self.files_df.to_dict(orient="records"),
                            stream=file, default_flow_style=False, sort_keys=False)
        self.files_df = None

    def loadDataInstance(self):
        with open(self.olddata_path, 'r') as file:
            self.files_df = pd.json_normalize(yaml.load(file, Loader=yaml.FullLoader))

    def filterData(self):
        actual_files = set(os.listdir(self.file_path))
        self.files_df = self.files_df[
            self.files_df["File_Name"].isin(actual_files).reset_index(drop=True)
        ]

    def setFilePath(self, path):
        self.file_path = path

    def getFilePath(self):
        return self.file_path

    def resourcePath(self, relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)