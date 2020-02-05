##############################
#   Author: Maanus Gulia
#   email:  mgulia@purdue.edu
#   ID:     ee364b04
#   Date:   11/27/19
##############################

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
        self.objLoadStartingImage.clicked.connect(self.loadDataLeft)
        self.objLoadEndingImage.clicked.connect(self.loadDataRight)
        self.leftTextPath = ''
        self.rightTextPath = ''
        self.leftPicPath = ''
        self.rightPicPath = ''
        self.leftFlag = False
        self.rightFlag = False
        self.toggleLR = False
        self.leftGreen = False
        self.rightGreen = False
        self.alphaVal = 0
        self.objShowTriangle.stateChanged.connect(self.showTriangles)
        self.objButtonBlend.clicked.connect(self.blendImage)
        self.objGraphicLeft.mousePressEvent = self.plottingPointsLeft
        self.objGraphicRight.mousePressEvent = self.plottingPointsRight
        self.mousePressEvent = self.clickedAnywhere
        self.keyPressEvent = self.backSpaceHelper
        self.backSpaceLeft = None
        self.backSpaceRight = None
        self.leftCoordX = []
        self.leftCoordY = []
        self.rightCoordX = []
        self.rightCoordY = []


    def loadDataLeft(self):
        filePath, _=QFileDialog.getOpenFileName(self, caption="Load Image Left")
        if not filePath:
            return
        self.loadStart(filePath)


    def loadDataRight(self):
        filePath, _ = QFileDialog.getOpenFileName(self, caption="Load Image Right")
        if not filePath:
            return
        self.loadEnd(filePath)


    def loadStart(self, filePath):
        self.leftScene = QGraphicsScene()
        self.leftScene.addPixmap(QPixmap(filePath))
        self.objGraphicLeft.setScene(self.leftScene)
        self.objGraphicLeft.fitInView(self.leftScene.sceneRect(), QtCore.Qt.KeepAspectRatio)

        self.leftFlag = True
        self.leftPicPath = filePath
        leftPointPath = filePath + '.txt'

        if (os.path.exists(leftPointPath)):
            self.leftTextPath = leftPointPath
            with open(self.leftTextPath, 'r') as FILE:
                dataFile = FILE.readlines()

            #wont work if operating on empty file with no points
            coordX = []
            coordY = []
            for idx, line in enumerate(dataFile):
                temp = line.split()
                coordX.append(temp[0])
                coordY.append(temp[1])

            for x, y in zip(coordX, coordY):
                self.leftScene.addEllipse(float(x), float(y), 15, 15, QtGui.QPen(QtCore.Qt.red), QtGui.QBrush(QtCore.Qt.red))

        self.bothLoaded()


    def loadEnd(self, filePath):
        self.rightScene = QGraphicsScene()
        self.rightScene.addPixmap(QPixmap(filePath))
        self.objGraphicRight.setScene(self.rightScene)
        self.objGraphicRight.fitInView(self.rightScene.sceneRect(), QtCore.Qt.KeepAspectRatio)
        self.rightFlag = True
        self.rightPicPath = filePath
        rightPointPath = filePath + '.txt'

        if (os.path.exists(rightPointPath)):
            self.rightTextPath = rightPointPath
            with open(rightPointPath, 'r') as FILE:
                dataFile = FILE.readlines()

            #wont work if operating on open file with no points
            coordX = []
            coordY = []
            for idx, line in enumerate(dataFile):
                temp = line.split()
                coordX.append(temp[0])
                coordY.append(temp[1])

            for x, y in zip(coordX, coordY):
                self.rightScene.addEllipse(float(x), float(y), 15, 15, QtGui.QPen(QtCore.Qt.red), QtGui.QBrush(QtCore.Qt.red))

        self.bothLoaded()


    def bothLoaded(self):
        if self.leftFlag and self.rightFlag:
            self.objButtonBlend.setEnabled(True)
            self.right00.setEnabled(True)
            self.horizontalSlider.setEnabled(True)
            self.horizontalSlider.valueChanged.connect(self.alphaBar)
            self.objShowTriangle.setEnabled(True)

    def alphaBar(self):
        num = self.horizontalSlider.value()/100
        num = round(num*2.0, 1) / 2.0
        self.right00.setText(str(num))
        self.alphaVal = num


    def showTriangles(self):
        #if self.objShowTriangle.isChecked() and os.path.exists(self.leftTextPath) and os.path.exists(self.rightTextPath):
        if self.objShowTriangle.isChecked() and os.path.exists(self.leftPicPath + '.txt') and os.path.exists(self.rightPicPath + '.txt'):

            self.leftTextPath = self.leftPicPath + '.txt'
            self.rightTextPath = self.rightPicPath + '.txt'

            leftTri, rightTri = loadTriangles(self.leftTextPath, self.rightTextPath)

            for x in leftTri:
                self.leftScene.addLine(x.vertices[0][0], x.vertices[0][1], x.vertices[1][0], x.vertices[1][1],
                                       QtGui.QPen(QtCore.Qt.red))
                self.leftScene.addLine(x.vertices[2][0], x.vertices[2][1], x.vertices[1][0], x.vertices[1][1],
                                       QtGui.QPen(QtCore.Qt.red))
                self.leftScene.addLine(x.vertices[2][0], x.vertices[2][1], x.vertices[0][0], x.vertices[0][1],
                                       QtGui.QPen(QtCore.Qt.red))

            for y in rightTri:
                self.rightScene.addLine(y.vertices[0][0], y.vertices[0][1], y.vertices[1][0], y.vertices[1][1],
                                        QtGui.QPen(QtCore.Qt.red))
                self.rightScene.addLine(y.vertices[2][0], y.vertices[2][1], y.vertices[1][0], y.vertices[1][1],
                                        QtGui.QPen(QtCore.Qt.red))
                self.rightScene.addLine(y.vertices[2][0], y.vertices[2][1], y.vertices[0][0], y.vertices[0][1],
                                        QtGui.QPen(QtCore.Qt.red))
        else:
            for obj in self.leftScene.items():
                if isinstance(obj, QtWidgets.QGraphicsLineItem):
                    self.leftScene.removeItem(obj)

            for obj2 in self.rightScene.items():
                if isinstance(obj2, QtWidgets.QGraphicsLineItem):
                    self.rightScene.removeItem(obj2)


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


    def plottingPointsLeft(self, event):
        if self.toggleLR == False and os.path.exists(self.leftPicPath):
            var = self.objGraphicLeft.mapToScene(event.pos())
            self.backSpaceLeft = self.leftScene.addEllipse(var.x() - 10, var.y() - 10, 20, 20, QtGui.QPen(),
                                                           QtGui.QBrush(QtCore.Qt.green))

            if self.leftGreen and self.rightGreen:
                self.leftScene.addEllipse(self.pointOnLeft.x() - 10, self.pointOnLeft.y() - 10, 20, 20, QtGui.QPen(), QtGui.QBrush(QtCore.Qt.blue))
                self.rightScene.addEllipse(self.pointOnRight.x() - 10, self.pointOnRight.y() - 10, 20, 20, QtGui.QPen(), QtGui.QBrush(QtCore.Qt.blue))
                self.leftGreen = False
                self.rightGreen = False
                self.addPointsToFile()
            else:
                self.leftGreen = True

            self.toggleLR = True
            self.leftGreen = True
            self.pointOnLeft = var


    def plottingPointsRight(self, event):
        if self.toggleLR and os.path.exists(self.rightPicPath):
            var = self.objGraphicRight.mapToScene(event.pos())
            self.backSpaceRight = self.rightScene.addEllipse(var.x() - 10, var.y() - 10, 20, 20, QtGui.QPen(),
                                                             QtGui.QBrush(QtCore.Qt.green))
            self.toggleLR = False
            self.rightGreen = True
            self.pointOnRight = var


    def backSpaceHelper(self, event):
        var = event.key()
        if var == QtCore.Qt.Key_Backspace:

            if self.leftGreen and self.toggleLR:
                self.objGraphicLeft.scene().removeItem(self.backSpaceLeft)
                self.leftGreen = False
                self.toggleLR = False

            elif self.rightGreen and not self.toggleLR:
                self.objGraphicRight.scene().removeItem(self.backSpaceRight)
                self.rightGreen = False
                self.toggleLR = True


    def clickedAnywhere(self, event):
        if self.leftGreen and self.rightGreen:
            self.leftScene.addEllipse(self.pointOnLeft.x() - 10, self.pointOnLeft.y() - 10, 20, 20, QtGui.QPen(),
                                      QtGui.QBrush(QtCore.Qt.blue))
            self.rightScene.addEllipse(self.pointOnRight.x() - 10, self.pointOnRight.y() - 10, 20, 20, QtGui.QPen(),
                                       QtGui.QBrush(QtCore.Qt.blue))

            self.addPointsToFile()
            self.leftGreen = False
            self.rightGreen = False


    def addPointsToFile(self):
        xL = str(round(self.pointOnLeft.x(), 1))
        yL = str(round(self.pointOnLeft.y(), 1))
        xR = str(round(self.pointOnRight.x(), 1))
        yR = str(round(self.pointOnRight.y(), 1))

        xL = xL.rjust(8)
        yL = yL.rjust(8)
        xR = xR.rjust(8)
        yR = yR.rjust(8)

        with open(self.leftPicPath + '.txt', 'a+') as FILE_LEFT:
            FILE_LEFT.write(xL + yL + '\n')

        with open(self.rightPicPath + '.txt', 'a+') as FILE_RIGHT:
            FILE_RIGHT.write(xR + yR + '\n')

        self.showTriangles()


if __name__=="__main__":
    currentApp = QApplication(sys.argv)
    currentForm = MorphingApp()

    currentForm.show()
    currentApp.exec_()