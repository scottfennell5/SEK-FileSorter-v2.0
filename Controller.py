class Controller:

    FILES_ID = "files"
    TARGET_ID = "target"

    def __init__(self, dataHandler, sorter):
        self.dataHandler = dataHandler
        self.dataHandler.loadSettings()
        self.dataHandler.refreshData()
        self.sorter = sorter
        self.sorter.updateTargetPath(self.dataHandler.getTargetPath())
        self.observer = None

    def newObserver(self, observer):
        self.observer = observer

    def notifyObserver(self):
        self.observer.update()

    def createLogs(self):
        pass #logs when application closes

    def getDataCopy(self):
        return self.dataHandler.getDataCopy()

    def getPath(self, pathID):
        path = None
        match pathID:
            case self.FILES_ID:
                path = self.dataHandler.getFilePath()
            case self.TARGET_ID:
                path = self.dataHandler.getTargetPath()
            case _:
                print("invalid path ID")

        if path is None:
            return ""
        else:
            return path

    def setPath(self, pathID, path):
        if path == '':
            print("warning: setPath called with no specified path! No action was taken from controller")
            return
        match pathID:
            case self.FILES_ID:
                self.dataHandler.setFilePath(path)
                self.dataHandler.refreshData()
            case self.TARGET_ID:
                self.dataHandler.setTargetPath(path)
                self.sorter.updateTargetPath(path)


    def getBaseDirectory(self):
        return self.dataHandler.getBaseDirectory()

    def updateFiles(self):
        self.notifyObserver()

    def saveData(self):
        self.dataHandler.saveDataInstance()

    def loadData(self):
        self.dataHandler.loadDataInstance()

    def checkData(self):
        print(self.dataHandler.getDataCopy())

    def filterData(self):
        self.dataHandler.filterData()

    def saveSettings(self):
        self.dataHandler.saveSettings()

    def getSettings(self):
        self.dataHandler.loadSettings()

    def getResource(self,relative_path):
        return self.dataHandler.resourcePath(relative_path)