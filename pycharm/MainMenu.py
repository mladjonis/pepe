import sys
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit
from Config import Config

class Meni(QWidget):
    def __init__(self, QWidget, funcSinglePlayer, funcTwoPlayers):
        super().__init__()
        self.allWidgets = []
        self.qWidget = QWidget

        self.bgImg = QLabel(QWidget)
        pixmap = QPixmap(Config.spriteLocation + "MainMenu2.png") #prva verzija pozadine MainMenu.png
        pixmap = pixmap.scaled(Config.mapSize * Config.gridSize, Config.mapSize * Config.gridSize + 50)
        self.bgImg.setPixmap(pixmap)
        self.bgImg.setFocusPolicy(QtCore.Qt.NoFocus)

        self.mainButtons = self.GlavniMeniKojiSePrikazeNaPocetku(funcSinglePlayer, funcTwoPlayers)
        self.optionsElements = self.OptionsSubMenuInit(self.OptionsSubMenuHide)

    def GlavniMeniKojiSePrikazeNaPocetku(self, singlePlayerOnClick, twoPlayerOnClick):
        listaWidgeta = []
        listaWidgeta.append(self.AddButton("1PlayerWidget", "widgets1Player", 5, 200, 400, 70, singlePlayerOnClick))
        listaWidgeta.append(self.AddButton("2PlayerWidget", "widgets2Player", 5, 300, 400, 70, twoPlayerOnClick))
        listaWidgeta.append(self.AddButton("highscoresWidget", "widgetsHighscores", 5, 400, 400, 70))
        listaWidgeta.append(self.AddButton("optionsWidget", "widgetsOptions", 5, 500, 400, 70, self.OptionsSubMenuShow))
        listaWidgeta.append(self.AddButton("exitWidget", "widgetsExit", 5, 600, 400, 70, self.exitClicked))
        return listaWidgeta

    def OptionsSubMenuInit(self, exitMenuOnClick=None):
        optionsWidgets = []
        optionsWidgets.append(self.AddLabel("player1Name", 50, 200, "PLAYER 1:", hide=True))
        optionsWidgets.append(self.AddLabel("player2Name", 50, 300, "PLAYER 2:", hide=True))
        optionsWidgets.append(self.AddEditLine("player1NameTxt", 250, 185, 450, 95, "Player1", hide=True))
        optionsWidgets.append(self.AddEditLine("player2NameTxt", 250, 285, 450, 95, "Player2", hide=True))
        optionsWidgets.append(self.AddButton("okWidget", "widgetsOk", 50, 420, 400, 70, exitMenuOnClick, hide=True))
        return optionsWidgets

    def OptionsSubMenuShow(self):
        for btn in self.mainButtons:
            btn.hide()

        for element in self.optionsElements:
            element.show()

    #Fja koja se izvrsava prilikom klika na Ok button u okviru Options prozora
    def OptionsSubMenuHide(self):
        #uzima se ime iz textBoxa, znamo da je na ovoj poziciji plName
        if self.optionsElements[2] != None:
            Config.p1Name = self.optionsElements[2].text()
            self.optionsElements[2].clearFocus()

        # uzima se ime iz textBoxa, znamo da je na ovoj poziciji p2Name
        if self.optionsElements[3] != None:
            Config.p2Name = self.optionsElements[3].text()
            self.optionsElements[3].clearFocus()

        for element in self.optionsElements:
            element.hide()

        for btn in self.mainButtons:
            btn.show()

    def AddButton(self, objectName, sprite, x, y, width, height, onClick=None, hide=False):
        btn = QPushButton(self.qWidget)
        btn.setObjectName(objectName)
        btn.setStyleSheet(
            "QPushButton#"+objectName+" { border-image: url('sprites/"+sprite+".png') 0 0 0 0 stretch stretch;} QPushButton#"+objectName+":hover { border-image: url('sprites/"+sprite+"Hover.png') 0 0 0 0 stretch stretch;}")
        btn.resize(width, height)
        btn.move(x, y)
        if onClick != None:
            btn.clicked.connect(onClick)
        btn.setFocusPolicy(QtCore.Qt.NoFocus)
        if hide:
            btn.hide()

        self.allWidgets.append(btn)
        return btn

    def AddLabel(self, objectName, x, y, text, hide=False):
        lbl = QLabel(self.qWidget)
        lbl.setObjectName(objectName)
        lbl.move(x, y)
        lbl.setStyleSheet(
            "QLabel#"+objectName+" {background: rgb(255, 255, 255) transparent; color: 'White'; font-family: '" + Config.font_family + "'; font-size: 70px;}")
        lbl.setText(text)
        if hide:
            lbl.hide()
        self.allWidgets.append(lbl)
        return lbl

    def AddEditLine(self, objectName, x, y, width, height, text, hide=False):
        editLine = QLineEdit(self.qWidget)
        editLine.setObjectName(objectName)
        editLine.move(x, y)
        editLine.resize(width, height)
        editLine.setStyleSheet(
            "QLineEdit#"+objectName+" {background: rgba(152, 193, 42, 0.5); border: 5px solid #98C12A; color: 'White'; font-family: '" + Config.font_family + "'; font-size: 70px;}")
        editLine.setText(text)
        # Widgets.append(player1NameTxt)
        if hide:
            editLine.hide()
        self.allWidgets.append(editLine)
        return editLine
        
    def HideMainMenu(self):
        for widget in self.allWidgets:
            widget.hide()
        self.bgImg.hide()

    def ShowMainMenu(self):
        self.OptionsSubMenuHide()
        self.bgImg.show()

    def exitClicked(self):
        sys.exit(0)

