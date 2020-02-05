# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MorphingGUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QGraphicsScene, QApplication
from PyQt5.QtGui import QPixmap

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Ui_MainWindow")
        MainWindow.resize(1067, 802)
        self.objLoadStartingImage = QtWidgets.QPushButton(MainWindow)
        self.objLoadStartingImage.setGeometry(QtCore.QRect(90, 10, 181, 27))
        self.objLoadStartingImage.setObjectName("objLoadStartingImage")
        self.objLoadEndingImage = QtWidgets.QPushButton(MainWindow)
        self.objLoadEndingImage.setGeometry(QtCore.QRect(640, 10, 151, 27))
        self.objLoadEndingImage.setObjectName("objLoadEndingImage")
        self.objShowTriangle = QtWidgets.QCheckBox(MainWindow)
        self.objShowTriangle.setGeometry(QtCore.QRect(420, 340, 131, 22))
        self.objShowTriangle.setObjectName("objShowTriangle")
        self.objButtonBlend = QtWidgets.QPushButton(MainWindow)
        self.objButtonBlend.setGeometry(QtCore.QRect(430, 740, 111, 27))
        self.objButtonBlend.setObjectName("objButtonBlend")
        self.groupBox = QtWidgets.QGroupBox(MainWindow)
        self.groupBox.setGeometry(QtCore.QRect(170, 330, 111, 21))
        self.groupBox.setObjectName("groupBox")
        self.groupBox_2 = QtWidgets.QGroupBox(MainWindow)
        self.groupBox_2.setGeometry(QtCore.QRect(790, 340, 101, 21))
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_3 = QtWidgets.QGroupBox(MainWindow)
        self.groupBox_3.setGeometry(QtCore.QRect(430, 700, 121, 21))
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalSlider = QtWidgets.QSlider(MainWindow)
        self.horizontalSlider.setGeometry(QtCore.QRect(130, 390, 721, 20))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider.setTickInterval(10)
        self.horizontalSlider.setMaximum(100)
        self.horizontalSlider.setSingleStep(5)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.label = QtWidgets.QLabel(MainWindow)
        self.label.setGeometry(QtCore.QRect(70, 390, 41, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(MainWindow)
        self.label_2.setGeometry(QtCore.QRect(130, 420, 31, 17))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(MainWindow)
        self.label_3.setGeometry(QtCore.QRect(830, 420, 41, 17))
        self.label_3.setObjectName("label_3")
        self.objGraphicLeft = QtWidgets.QGraphicsView(MainWindow)
        self.objGraphicLeft.setGeometry(QtCore.QRect(90, 40, 361, 281))
        self.objGraphicLeft.setObjectName("objGraphicLeft")




        self.objGraphicRight = QtWidgets.QGraphicsView(MainWindow)
        self.objGraphicRight.setGeometry(QtCore.QRect(640, 50, 371, 281))
        self.objGraphicRight.setObjectName("objGraphicsRight")
        self.objGraphicsBottom = QtWidgets.QGraphicsView(MainWindow)
        self.objGraphicsBottom.setGeometry(QtCore.QRect(360, 461, 281, 221))
        self.objGraphicsBottom.setObjectName("objGraphicsBottom")
        self.right00 = QtWidgets.QTextEdit(MainWindow)
        self.right00.setGeometry(QtCore.QRect(880, 380, 51, 31))
        self.right00.setObjectName("right00")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.objLoadStartingImage.setText(_translate("MainWindow", "Load Starting Image ..."))
        self.objLoadEndingImage.setText(_translate("MainWindow", "Load Ending Image ..."))
        self.objShowTriangle.setText(_translate("MainWindow", "Show Triangles"))
        self.objButtonBlend.setText(_translate("MainWindow", "Blend"))
        self.groupBox.setTitle(_translate("MainWindow", "Starting Image"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Ending Image"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Blending Result"))
        self.label.setText(_translate("MainWindow", "Alpha"))
        self.label_2.setText(_translate("MainWindow", "0.0"))
        self.label_3.setText(_translate("MainWindow", "1.0"))
        self.right00.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Sans\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>"))

