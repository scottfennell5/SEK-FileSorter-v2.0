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

    def __init__(self):
        self.files_df = pd.DataFrame(self.files_dict)
        self.olddata_path = self.resourcePath(r"PersistentData\Data\olddata.yaml")
        self.settings_path = self.resourcePath(r"PersistentData\Data\settings.yaml")
        self.file_path = ""
        self.target_path = ""

    def getDataCopy(self):
        return self.files_df.copy()

    def loadSettings(self):
        with open(self.settings_path, 'r') as file:
            settings = yaml.load(file, Loader=yaml.FullLoader)

        self.file_path = settings["file_path"]
        if (self.file_path is None) or (not os.path.exists(self.file_path)):
            self.file_path = ""

        self.target_path = settings["target_path"]
        if (self.target_path is None) or (not os.path.exists(self.target_path)):
            self.target_path = ""

    def saveSettings(self):
        settings = {
            "file_path":self.file_path,
            "target_path":self.target_path
        }

        with open(self.settings_path, 'w') as file:
            yaml.dump(settings,
                      stream=file,
                      default_flow_style=False,
                      sort_keys=False)

    def saveDataInstance(self):
        with open(self.olddata_path,'w') as file:
            yaml.dump(self.files_df.to_dict(orient="records"),
                      stream=file,
                      default_flow_style=False,
                      sort_keys=False)

    def loadDataInstance(self):
        with open(self.olddata_path, 'r') as file:
            self.files_df = pd.json_normalize(yaml.load(file, Loader=yaml.FullLoader))

    def filterData(self):
        #Removes rows that correlate to files that no longer exist or cannot be found.
        if self.file_path == "":
            self.files_df = pd.DataFrame(self.files_dict)
            return

        actual_files = set(os.listdir(self.file_path))
        self.files_df = (self.files_df[self.files_df["File_Name"].isin(actual_files)].reset_index(drop=True))

    def scanFiles(self):
        if self.file_path == "":
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
                    'Client_Type': ['unknown'],
                    'First_Name': ['unknown client'],
                    'Second_Name': [None],
                    'Year': [1984],
                    'File_Description': ['unknown']
                })
                self.files_df = pd.concat([self.files_df, new_row], ignore_index=True)

    def refreshData(self):
        self.loadDataInstance()
        self.filterData()
        self.scanFiles()

    def setFilePath(self, path):
        self.file_path = path

    def getFilePath(self):
        return self.file_path

    def setTargetPath(self, path):
        self.target_path = path

    def getTargetPath(self):
        return self.target_path

    def getBaseDirectory(self):
        return self.resourcePath("")

    def resourcePath(self, relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def populateTempData(self):
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