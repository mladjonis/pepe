from Config import Config
from PyQt5 import QtCore
import time


class GameObject:
    allGameObjects = []

    def __init__(self):
        self.allGameObjects.append(self)

    def update(self):
        pass


class GOUpdater(QtCore.QThread):
    nekiObjekat = QtCore.pyqtSignal(object)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.updaterThreadWork = True

    def run(self):
        while self.updaterThreadWork:
            for gameObject in GameObject.allGameObjects:
                #gameObject.update()
                self.nekiObjekat.emit(gameObject)
            time.sleep(1 / Config.FPS)