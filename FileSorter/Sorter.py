import yaml

class Sorter:
    def __init__(self):
        self.target_path = r""
        print("init sorter complete")

    def setTargetPath(self,path):
        self.target_path=path

    def sortFile(self,file_info):
        pass #file_info is a row from the files dataframe