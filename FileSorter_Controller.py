class Controller:

    def __init__(self, dataHandler, sorter):
        self.dataHandler = dataHandler
        dataHandler.scanFiles()
        self.sorter = sorter
        self.observers = []
        print("init controller complete")

    def addObserver(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def removeObserver(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def notifyObservers(self):
        for observer in self.observers:
            observer.update()

    def createLogs(self):
        print("creating logs...")

    def getFiles(self):
        return self.dataHandler.getFiles()

    def verify(self):
        print("controller good!")
        self.dataHandler.verify()
        self.sorter.verify()

    def updateFiles(self):
        self.notifyObservers()