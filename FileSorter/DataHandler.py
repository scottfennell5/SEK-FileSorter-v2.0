import pandas as pd
import yaml
from os import path

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
        self.file_path = ""
        data_dir = path.join(path.dirname(path.realpath(__file__)),"PersistentData")
        self.olddata_path = path.join(data_dir,"olddata.yaml")
        self.settings_path = path.join(data_dir,"settings.yaml")
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
                    'First_Name': ['unknown'],
                    'Second_Name': [None],
                    'Year': [1984],
                    'File_Description': ['unknown']
                })
            self.files_df = pd.concat([self.files_df, new_row], ignore_index=True)
        print(self.files_df)

    def getFiles(self):
        return self.files_df.copy()

    def readSettings(self):
        pass

    def saveSettings(self):
        pass

    def saveDataInstance(self):
        yaml_output = yaml.dump(self.files_df.to_dict(orient="index"), sort_keys=False)
        print(yaml_output)

    def setFilePath(self, path):
        self.file_path = path