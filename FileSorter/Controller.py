class Controller:

    def __init__(self, dataHandler, sorter):
        self.dataHandler = dataHandler
        dataHandler.scanFiles()
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

    def verify(self):
        print("controller good!")
        self.dataHandler.verify()
        self.sorter.verify()

    def updateFiles(self):
        self.notifyObserver()