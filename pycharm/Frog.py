from Rectangle import Rectangle
from PyQt5.QtCore import Qt

from Config import Config
import time

class Frog(Rectangle):
    # height = 50
    # width = 50
    height = Config.gridSize
    width = Config.gridSize

    spriteUpP1 = 'frog_sprite_50.png'
    spriteLeftP1 = 'frog_sprite_l_50.png'
    spriteRightP1 = 'frog_sprite_r_50.png'
    spriteDownP1 = 'frog_sprite_d_50.png'

    spriteUpP2 = 'frog_sprite_player2_50.png'
    spriteLeftP2 = 'frog_sprite_player2l_50.png'
    spriteRightP2 = 'frog_sprite_player2r_50.png'
    spriteDownP2 = 'frog_sprite_player2d_50.png'

    def __init__(self, x, y, isPlayerTwo = False):
        self.startX = x
        self.startY = y
        self.logSpeed = 0
        self.lives = Config.frogLives
        self.sprite = self.spriteUpP1
        if isPlayerTwo:
            self.sprite = self.spriteUpP2

        super().__init__(x * Config.gridSize,y * Config.gridSize,self.height,self.width, self.sprite, layer=Config.layerZabe)
        self.isPlayerTwo = isPlayerTwo
        self.Show()

    def update(self):
        if self.IsInWaterLane():
            if self.IsOnLog():
                # kad je zaba na drvetu i dodje do ivice ekrana, da zaba klizi po drvetu (ne menja svoju poziciju)
                if (self.x > Config.gridSize * Config.mapSize - self.w and self.logSpeed > 0) or (self.x < 1 and self.logSpeed < 0):
                    return

                self.SetPosition(self.x + self.logSpeed, self.y)
            else:
                self.Die()
        else:
            if self.CollidedWithObstacle():
                self.Die()

        lokvanj = self.CollidedWithLilypad()
        if lokvanj != None:
            lokvanj.usedByPlayer(self)

    def CollidedWithLilypad(self):
        return self.CollisionLayerSpecific(Config.layerLilypad, returnObject=True)

    def CollidedWithObstacle(self):
        return self.CollisionLayerSpecific(Config.layerPrepreke)

    def IsOnLog(self):
        objCollidedWith = self.CollisionLayerSpecific(Config.layerDrva, returnObject=True)
        if objCollidedWith != None:
            self.logSpeed = objCollidedWith.speed
            return True
        return False

    def IsInWaterLane(self):
        return self.CollisionLayerSpecific(Config.layerWaterLane)

    def Die(self):
        self.lives -= 1

        if self.lives > 0:
            self.ReturnToStart()

    def ReturnToStart(self):
        self.SetPosition(self.startX * Config.gridSize, self.startY * Config.gridSize)
        if self.isPlayerTwo:
            self.ChangeSprite(self.spriteUpP2)
        else:
            self.ChangeSprite(self.spriteUpP1)

    def Move(self, x,y):
        currentPosition = super().GetPosition()
        newXcoord = currentPosition[0] + Config.gridSize * x
        newYcoord = currentPosition[1] + Config.gridSize * y
        super().SetPosition(newXcoord, newYcoord)

    def GoLeft(self):
        if self.isPlayerTwo:
            self.ChangeSprite(self.spriteLeftP2)
        else:
            self.ChangeSprite(self.spriteLeftP1)

        if self.x == 0 :
            return

        if not self.IsEmpty(-1,0):
            return

        self.Move(-1,0)

    def GoRight(self):
        if self.isPlayerTwo:
            self.ChangeSprite(self.spriteRightP2)
        else:
            self.ChangeSprite(self.spriteRightP1)

        if self.x == Config.gridSize * (Config.mapSize - 1):
            return

        if not self.IsEmpty(1,0):
            return

        self.Move(1,0)

    def GoUp(self):
        if self.isPlayerTwo:
            self.ChangeSprite(self.spriteUpP2)
        else:
            self.ChangeSprite(self.spriteUpP1)

        if self.y == 0:
            return

        self.CorrectXPositionToGrid()

        if not self.IsEmpty(0,-1):
            return

        self.Move(0,-1)

    def GoDown(self):
        if self.isPlayerTwo:
            self.ChangeSprite(self.spriteDownP2)
        else:
            self.ChangeSprite(self.spriteDownP1)

        self.CorrectXPositionToGrid()

        if self.y == Config.gridSize * (Config.mapSize - 1):
            return

        if not self.IsEmpty(0,1):
            return

        self.Move(0,1)

    def CorrectXPositionToGrid(self):
        if self.x % Config.gridSize >= 25:
            newX = self.x + (Config.gridSize - (self.x % Config.gridSize))
            self.SetPosition(newX, self.y)
        else:
            newX = self.x - (self.x % Config.gridSize)
            self.SetPosition(newX, self.y)

    def KeyPress(self, key):
        if self.isPlayerTwo:
            if key == Qt.Key_D:
                self.GoRight()
            elif key == Qt.Key_S:
                self.GoDown()
            elif key == Qt.Key_W:
                self.GoUp()
            elif key == Qt.Key_A:
                self.GoLeft()
        else:
            if key == Qt.Key_Right:
                self.GoRight()
            elif key == Qt.Key_Down:
                self.GoDown()
            elif key == Qt.Key_Up:
                self.GoUp()
            elif key == Qt.Key_Left:
                self.GoLeft()