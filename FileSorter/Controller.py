class Controller:

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

    def getFiles(self):
        return self.dataHandler.getFiles()

    def updateFiles(self):
        self.notifyObserver()

    def test(self):
        self.dataHandler.saveDataInstance()