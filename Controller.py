class Controller:

    FILES_ID = "files"
    TARGET_ID = "target"

    def __init__(self, dataHandler, sorter):
        self.dataHandler = dataHandler
        dataHandler.scanFiles()
        #self.settings=dataHandler.getSettings()
        self.sorter = sorter
        self.observer = None
        print("init controller complete")

    def newObserver(self, observer):
        self.observer = observer

    def notifyObserver(self):
        self.observer.update()

    def createLogs(self):
        print("creating logs...")

    def getDataCopy(self):
        return self.dataHandler.getDataCopy()

    def getPath(self, pathID):
        match pathID:
            case self.FILES_ID:
                path = self.dataHandler.getFilePath()
            case self.TARGET_ID:
                path = self.sorter.getTargetPath()

        if path == None:
            return "no path found!"
        else:
            return path

    def setPath(self, pathID, path):
        match pathID:
            case self.FILES_ID:
                self.dataHandler.setFilePath(path)
            case self.TARGET_ID:
                self.sorter.setTargetPath(path)

    def updateFiles(self):
        self.notifyObserver()

    def saveData(self):
        self.dataHandler.saveDataInstance()

    def loadData(self):
        self.dataHandler.loadDataInstance()

    def checkData(self):
        print(self.dataHandler.getDataCopy())

    def filter(self):
        self.dataHandler.filterData()

    def getResource(self,relative_path):
        return self.dataHandler.resourcePath(relative_path)