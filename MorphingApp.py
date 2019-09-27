import os
import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QGraphicsScene
from MorphingGUI import *
from Morphing import *
import numpy as np
from PIL import ImageQt, Image
from MorphingGUI import *
from PyQt5 import QtCore, QtGui
import imageio as im





class MorphingApp(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        self.flag = 0
        super(MorphingApp, self).__init__(parent)
        self.setupUi(self)
        self.scene = None
        self.sceneLeft = None
        self.sceneRight = None

        self.objShowTriangle.setDisabled(True)
        self.right00.setDisabled(True)
        self.objButtonBlend.setDisabled(True)
        self.horizontalSlider.setDisabled(True)
        self.objLoadStartingImage.setEnabled(True)
        self.objLoadEndingImage.setEnabled(True)
        self.objLoadStartingImage.clicked.connect(self.loadData)
        self.objLoadEndingImage.clicked.connect(self.loadData2)
        self.leftTextPath = ''
        self.rightTextPath = ''
        self.leftPicPath = ''
        self.rightPicPath = ''
        self.objShowTriangle.stateChanged.connect(self.showTriangles)
        self.objButtonBlend.clicked.connect(self.blendImage)
        self.alphaVal = 0
        self.leftTempData = None
        self.leftData = []
        self.rightTempData = None
        self.rightData = []


        self.objGraphicLeft.mousePressEvent = self.plottingPointsLeft
        self.objGraphicRight.mousePressEvent = self.plottingPointsRight
        self.mousePressEvent = self.anywhere
        self.holder = 0
        self.bothClicked = 0
        self.leftGreenX = None
        self.leftGreenY = None
        self.rightGreenX = None
        self.rightGreenY = None
        self.countLeft = 0
        self.countRight = 0
        self.count1 = 0
        self.leftGreenXAny = None
        self.leftGreenYAny = None
        self.rightGreenXAny = None
        self.rightGreenYAny = None
        self.backSpaceLeft = None
        self.backSpaceRight = None

        self.leftCoordX = []
        self.leftCoordY = []

        self.rightCoordX = []
        self.rightCoordY = []
        self.newLine = 0
        self.newLine2 = 0

        self.newLineFlag = 0
        self.backLeftFlag = 0
        self.backRightFlag = 0



    def addPointsToFileLeft(self):


        for x, y in zip(self.leftCoordX, self.leftCoordY):
            x = str(round(x, 1))
            y = str(round(y, 1))
            x = x.rjust(8)
            y = y.rjust(8)

            if  os.path.exists(self.leftPicPath + '.txt'):
                with open(self.leftPicPath + '.txt', 'a+') as FILE:
                    FILE.write('\n' + x + y)

            else:
                with open(self.leftPicPath + '.txt', 'a+') as FILE:
                    FILE.write(x + y)


    def addPointsToFileRight(self):


        for x, y in zip(self.rightCoordX, self.rightCoordY):
            x = str(round(x, 1))
            y = str(round(y, 1))
            x = x.rjust(8)
            y = y.rjust(8)

            if  os.path.exists(self.rightPicPath + '.txt'):
                with open(self.rightPicPath + '.txt', 'a+') as FILE:

                    FILE.write('\n' + x + y)

            else:
                with open(self.rightPicPath + '.txt', 'a+') as FILE:
                    FILE.write(x + y)


    def backSpaceHelper1(self, event):
        var = event.key()
        if var == QtCore.Qt.Key_Backspace:
            self.objGraphicLeft.scene().removeItem(self.backSpaceLeft)
            self.backLeftFlag = 1

    def backSpaceHelper2(self, event):
        var = event.key()

        if var == QtCore.Qt.Key_Backspace:
            self.objGraphicRight.scene().removeItem(self.backSpaceRight)
            self.backRightFlag = 1


    def plottingPointsLeft(self, event):

        if(self.holder % 2 is 0):
            self.countLeft += 1
            var = self.objGraphicLeft.mapToScene(event.pos())
            self.leftTempData = var
            self.leftData.append(var)
            self.leftGreenX = self.leftData[self.countLeft - 2].x()
            self.leftGreenY = self.leftData[self.countLeft - 2].y()
            self.backSpaceLeft = self.leftScene.addEllipse(var.x() - 10, var.y() - 10, 20, 20, QtGui.QPen(), QtGui.QBrush(QtCore.Qt.green))
            self.objGraphicLeft.keyPressEvent = self.backSpaceHelper1
            self.holder += 1
            self.bothClicked += 1

            if(self.bothClicked % 3 == 0):
                self.leftScene.addEllipse(self.leftGreenX - 10, self.leftGreenY - 10, 20, 20, QtGui.QPen(), QtGui.QBrush(QtCore.Qt.blue))
                #Appending points for blue points

                self.leftCoordX.append(self.leftGreenX)
                self.leftCoordY.append(self.leftGreenY)

                if (self.countLeft>1):
                    self.rightScene.addEllipse(self.rightGreenX - 10, self.rightGreenY - 10, 20, 20, QtGui.QPen(), QtGui.QBrush(QtCore.Qt.blue))

                self.bothClicked += 1
                self.rightGreenX = self.rightData[self.countRight - 1].x()
                self.rightGreenY = self.rightData[self.countRight - 1].y()
                self.backSpaceRight =  self.rightScene.addEllipse(self.rightGreenX - 10, self.rightGreenY - 10, 20, 20, QtGui.QPen(), QtGui.QBrush(QtCore.Qt.blue))
                self.objGraphicRight.keyPressEvent = self.backSpaceHelper2

                #Appending points for blue points
                self.rightCoordX.append(self.rightGreenX)
                self.rightCoordY.append(self.rightGreenY)

            self.count1 += 1
            self.addPointsToFileLeft()
            self.addPointsToFileRight()
            self.showTriangles()


    def anywhere(self, event):
        if (self.count1 % 2 is 0):

            self.leftGreenX = self.leftData[self.countLeft - 1].x()
            self.leftGreenY = self.leftData[self.countLeft - 1].y()

            self.leftCoordX.append(self.leftGreenX)
            self.leftCoordY.append(self.leftGreenY)
            if (self.backLeftFlag is 1):
                self.leftCoordX = self.leftCoordX[:-1]
                self.leftCoordY = self.leftCoordY[:-1]
                self.backLeftFlag = 0

            self.backSpaceLeft = self.leftScene.addEllipse(self.leftGreenX - 10, self.leftGreenY - 10, 20, 20, QtGui.QPen(), QtGui.QBrush(QtCore.Qt.blue))

            self.objGraphicLeft.keyPressEvent = self.backSpaceHelper1

            if (self.countLeft > 1):
                self.backSpaceRight = self.rightScene.addEllipse(self.rightGreenX - 10, self.rightGreenY - 10, 20, 20, QtGui.QPen(), QtGui.QBrush(QtCore.Qt.blue))
                self.objGraphicRight.keyPressEvent = self.backSpaceHelper2

            self.rightGreenX = self.rightData[self.countRight - 1].x()
            self.rightGreenY = self.rightData[self.countRight - 1].y()

            self.rightCoordX.append(self.rightGreenX)
            self.rightCoordY.append(self.rightGreenY)
            if (self.backRightFlag is 1):
                self.rightCoordX = self.rightCoordX[:-1]
                self.rightCoordY = self.rightCoordY[:-1]
                self.backrightFlag = 0

            self.backSpaceRight = self.rightScene.addEllipse(self.rightGreenX - 10, self.rightGreenY - 10, 20, 20, QtGui.QPen(), QtGui.QBrush(QtCore.Qt.blue))
            self.objGraphicRight.keyPressEvent = self.backSpaceHelper2

            self.addPointsToFileLeft()
            self.addPointsToFileRight()
            self.showTriangles()



    def plottingPointsRight(self, event):

        if(self.holder % 2 is 1):
            var = self.objGraphicRight.mapToScene(event.pos())
            self.countRight += 1
            #print(var)
            self.rightTempData = var
            self.rightData.append(var)

            self.rightGreenX = self.rightData[self.countRight - 2].x()
            self.rightGreenY = self.rightData[self.countRight - 2].y()

            self.backSpaceRight = self.rightScene.addEllipse(var.x() - 10, var.y() - 10, 20, 20, QtGui.QPen(), QtGui.QBrush(QtCore.Qt.green))

            self.objGraphicRight.keyPressEvent = self.backSpaceHelper2

            self.holder += 1
            self.bothClicked += 1
            self.count1 += 1



    def blendImage(self):


        left, right = loadTriangles(self.leftTextPath, self.rightTextPath)

        leftTri = np.array(imageio.imread(self.leftPicPath), np.uint8)
        rightTri = np.array(imageio.imread(self.rightPicPath), np.uint8)

        objM = Morpher(leftTri, left, rightTri, right)
        targetImage = objM.getImageAtAlpha(self.alphaVal)

        self.bottomScene = QGraphicsScene()
        varImage = Image.fromarray(targetImage.astype(np.uint8))
        varQ = QtGui.QImage(ImageQt.ImageQt(varImage))

        show = QtGui.QPixmap.fromImage(varQ)
        self.bottomScene.addPixmap(QtGui.QPixmap(show))
        self.objGraphicsBottom.setScene(self.bottomScene)
        self.objGraphicsBottom.fitInView(self.bottomScene.sceneRect(), QtCore.Qt.KeepAspectRatio)



    def showTriangles(self):

        leftTri, rightTri = loadTriangles(self.leftPicPath + '.txt', self.rightPicPath + '.txt')

        if self.objShowTriangle.isChecked():
            for x in leftTri:
                self.leftScene.addLine(x.vertices[0][0], x.vertices[0][1], x.vertices[1][0], x.vertices[1][1], QtGui.QPen(QtCore.Qt.red))
                self.leftScene.addLine(x.vertices[2][0], x.vertices[2][1], x.vertices[1][0], x.vertices[1][1], QtGui.QPen(QtCore.Qt.red))
                self.leftScene.addLine(x.vertices[2][0], x.vertices[2][1], x.vertices[0][0], x.vertices[0][1], QtGui.QPen(QtCore.Qt.red))

            for y in rightTri:
                self.rightScene.addLine(y.vertices[0][0], y.vertices[0][1], y.vertices[1][0], y.vertices[1][1], QtGui.QPen(QtCore.Qt.red))
                self.rightScene.addLine(y.vertices[2][0], y.vertices[2][1], y.vertices[1][0], y.vertices[1][1], QtGui.QPen(QtCore.Qt.red))
                self.rightScene.addLine(y.vertices[2][0], y.vertices[2][1], y.vertices[0][0], y.vertices[0][1], QtGui.QPen(QtCore.Qt.red))
        else:
            for obj in self.leftScene.items():
                if isinstance(obj, QtWidgets.QGraphicsLineItem):
                    self.leftScene.removeItem(obj)

            for obj2 in self.rightScene.items():
                if isinstance(obj2, QtWidgets.QGraphicsLineItem):
                    self.rightScene.removeItem(obj2)





    def loadData(self):
        filePath, _=QFileDialog.getOpenFileName(self, caption='Open PNG file ...', filter="PNG files (*.png)")

        if not filePath:
            return

        self.loadStart(filePath)

    def loadData2(self):
        filePath, _=QFileDialog.getOpenFileName(self, caption='Open PNG file ...', filter="PNG files (*.png)")

        if not filePath:
            return

        self.loadEnd(filePath)

    def loadStart(self, filePath):

        self.leftScene = QGraphicsScene()
        self.leftScene.addPixmap(QPixmap(filePath))
        self.objGraphicLeft.setScene(self.leftScene)
        self.objGraphicLeft.fitInView(self.leftScene.sceneRect(), QtCore.Qt.KeepAspectRatio)


        self.flag += 1;

        if self.flag == 2:
            self.objButtonBlend.setEnabled(True)
            self.right00.setEnabled(True)
            self.horizontalSlider.setEnabled(True)
            self.horizontalSlider.valueChanged.connect(self.alphaBar)
            self.objShowTriangle.setEnabled(True)

        self.leftPicPath = filePath
        leftPointPath = filePath + '.txt'
        self.leftTextPath = leftPointPath

        if (os.path.exists(leftPointPath)):
            self.newLineFlag += 1
            with open(leftPointPath, 'r') as FILE:
                dataFile = FILE.readlines()

            coordX = []
            coordY = []
            for idx, line in enumerate(dataFile):
                temp = line.split()
                coordX.append(temp[0])
                coordY.append(temp[1])

            for x, y in zip(coordX, coordY):
                self.leftScene.addEllipse(float(x), float(y), 15, 15, QtGui.QPen(QtCore.Qt.red), QtGui.QBrush(QtCore.Qt.red))



    def loadEnd(self, filePath):
        self.rightScene = QGraphicsScene()
        self.rightScene.addPixmap(QPixmap(filePath))
        self.objGraphicRight.setScene(self.rightScene)
        self.objGraphicRight.fitInView(self.rightScene.sceneRect(), QtCore.Qt.KeepAspectRatio)

        self.flag += 1;

        if self.flag == 2:
            self.objButtonBlend.setEnabled(True)
            self.right00.setEnabled(True)
            self.horizontalSlider.setEnabled(True)
            self.horizontalSlider.valueChanged.connect(self.alphaBar)
            self.objShowTriangle.setEnabled(True)

        self.rightPicPath = filePath
        rightPointPath = filePath + '.txt'
        self.rightTextPath = rightPointPath

        if (os.path.exists(rightPointPath)):
            self.newLineFlag = 1
            with open(rightPointPath, 'r') as FILE:
                dataFile = FILE.readlines()

            coordX = []
            coordY = []
            for idx, line in enumerate(dataFile):
                temp = line.split()
                coordX.append(temp[0])
                coordY.append(temp[1])

            for x, y in zip(coordX, coordY):
                self.rightScene.addEllipse(float(x), float(y), 15, 15, QtGui.QPen(QtCore.Qt.red), QtGui.QBrush(QtCore.Qt.red))



    def alphaBar(self):
        self.right00.setText(str(self.horizontalSlider.value()/100))
        self.alphaVal = self.horizontalSlider.value()/100




if __name__=="__main__":
    currentApp = QApplication(sys.argv)
    currentForm = MorphingApp()

    currentForm.show()
    currentApp.exec_()
