import os
import sys
import numpy as np
from scipy.interpolate import RectBivariateSpline
from scipy.spatial import Delaunay
import scipy.interpolate
from PIL import Image, ImageDraw
import matplotlib.pyplot as plt
import imageio


class Triangle:
    def __init__(self, vertices):
        self.vertices = vertices
        if (vertices.dtype != np.float64):
            raise ValueError("Input needs to be of type float64")
        if (vertices.shape != (3,2)):
            raise ValueError("Not the right dimensions")

    def getPoints(self):

        var1 = int(self.vertices[0, 0])
        var2 = int(self.vertices[1, 0])
        var3 = int(self.vertices[2, 0])
        car1 = int(self.vertices[0, 1])
        car2 = int(self.vertices[1, 1])
        car3 = int(self.vertices[2, 1])

        minX = min(var1, var2, var3)
        maxX = max(var1, var2, var3)
        maxY = max(car1, car2, car3)
        minY = min(car1, car2, car3)

        output = []
        for loop1 in range(int(minX), int(maxX) + 1):
            for loop2 in range(int(minY), int(maxY) + 1):
                x1 = (var2 - var1) * (loop2 - car1) - (car2 - car1) * (loop1 - var1)
                x2 = (var3 - var2) * (loop2 - car2) - (car3 - car2) * (loop1 - var2)
                x3 = (var1 - var3) * (loop2 - car3) - (car1 - car3) * (loop1 - var3)
                if (x1 < 0 and x2 < 0 and x3 < 0) or (x1 > 0 and x2 > 0 and x3 > 0):
                    output.append([loop1, loop2])

        return np.asarray(output, dtype=np.float64)


def loadTriangles(leftPointFilePath, rightPointFilePath):

    with open(leftPointFilePath, 'r') as FILE:
        leftData = FILE.readlines()

    with open(rightPointFilePath, 'r') as FILE:
        rightData = FILE.readlines()

    leftPoints = []
    rightPoints = []

    for x in leftData:
        temp = x.split()
        tempLeft = []
        tempLeft.append(float(temp[0]))
        tempLeft.append(float(temp[1]))

        leftPoints.append(tempLeft)

    for y in rightData:
        temp = y.split()
        tempRight = []
        tempRight.append(float(temp[0]))
        tempRight.append(float(temp[1]))

        rightPoints.append(tempRight)

    triLeft = np.asarray(leftPoints, dtype=np.float64)
    triRight = np.asarray(rightPoints, dtype=np.float64)

    leftDel = Delaunay(triLeft)

    leftFinal = [Triangle(vertices) for vertices in triLeft[leftDel.simplices].astype(np.float64)]
    rightFinal = [Triangle(vertices) for vertices in triRight[leftDel.simplices].astype(np.float64)]

    return(leftFinal, rightFinal)


class Morpher:

    def __init__(self, leftImage, leftTriangles, rightImage, rightTriangles):

        if type(leftTriangles) is not list:
            raise TypeError("Left Triangle needs to be of type List")

        if type(rightTriangles) is not list:
            raise TypeError("Right Triangle needs to be of type List")

        for x in leftTriangles:
            if not isinstance(x, Triangle):
                raise TypeError("Data in left triangle is not of type Triangle")

        for y in rightTriangles:
            if not isinstance(y, Triangle):
                raise TypeError("Data in the right triangle is not of type Triangle")

        if (leftImage.dtype != np.uint8):
            raise TypeError("Left Image must be of type uint8")

        if (rightImage.dtype != np.uint8):
            raise TypeError("Left Image must be of type uint8")

        self.leftImage = leftImage
        self.leftTriangle = leftTriangles
        self.rightImage = rightImage
        self.rightTriangle = rightTriangles


    def getImageAtAlpha(self, alpha):

        picture = np.zeros(self.rightImage.shape, np.uint8)
        splineLeft = RectBivariateSpline(x=np.arange(0, self.leftImage.shape[0]), y=np.arange(0, self.leftImage.shape[1]), z=self.leftImage)
        splineRight = RectBivariateSpline(x=np.arange(0, self.rightImage.shape[0]), y=np.arange(0, self.rightImage.shape[1]), z=self.rightImage)


        imageLeft = np.zeros(self.leftImage.shape, np.uint8)
        imageRight = np.zeros(self.rightImage.shape, np.uint8)


        for leftTri, rightTri in zip(self.leftTriangle, self.rightTriangle):
            temp = np.asarray(((1-alpha)*leftTri.vertices) + (alpha*rightTri.vertices), dtype=np.float64)

            capB = temp.reshape((3,2))
            bVal = capB.reshape((6,1))

            aLMatrix = np.zeros((6,6))

            aLMatrix[0, 0] = leftTri.vertices[0][0]
            aLMatrix[0, 1] = leftTri.vertices[0][1]
            aLMatrix[0, 2] = 1
            aLMatrix[1, 3] = leftTri.vertices[0][0]
            aLMatrix[1, 4] = leftTri.vertices[0][1]
            aLMatrix[1, 5] = 1
            aLMatrix[2, 0] = leftTri.vertices[1][0]
            aLMatrix[2, 1] = leftTri.vertices[1][1]
            aLMatrix[2, 2] = 1
            aLMatrix[3, 3] = leftTri.vertices[1][0]
            aLMatrix[3, 4] = leftTri.vertices[1][1]
            aLMatrix[3, 5] = 1
            aLMatrix[4, 0] = leftTri.vertices[2][0]
            aLMatrix[4, 1] = leftTri.vertices[2][1]
            aLMatrix[4, 2] = 1
            aLMatrix[5, 3] = leftTri.vertices[2][0]
            aLMatrix[5, 4] = leftTri.vertices[2][1]
            aLMatrix[5, 5] = 1


            aRMatrix = np.zeros((6,6))
            aRMatrix[0, 0] = rightTri.vertices[0][0]
            aRMatrix[0, 1] = rightTri.vertices[0][1]
            aRMatrix[0, 2] = 1
            aRMatrix[1, 3] = rightTri.vertices[0][0]
            aRMatrix[1, 4] = rightTri.vertices[0][1]
            aRMatrix[1, 5] = 1
            aRMatrix[2, 0] = rightTri.vertices[1][0]
            aRMatrix[2, 1] = rightTri.vertices[1][1]
            aRMatrix[2, 2] = 1
            aRMatrix[3, 3] = rightTri.vertices[1][0]
            aRMatrix[3, 4] = rightTri.vertices[1][1]
            aRMatrix[3, 5] = 1
            aRMatrix[4, 0] = rightTri.vertices[2][0]
            aRMatrix[4, 1] = rightTri.vertices[2][1]
            aRMatrix[4, 2] = 1
            aRMatrix[5, 3] = rightTri.vertices[2][0]
            aRMatrix[5, 4] = rightTri.vertices[2][1]
            aRMatrix[5, 5] = 1

            leftH = np.linalg.solve(aLMatrix, bVal)
            rightH = np.linalg.solve(aRMatrix, bVal)

            leftH = np.append(leftH, 0)
            leftH = np.append(leftH, 0)
            leftH = np.append(leftH, 1)

            rightH = np.append(rightH, 0)
            rightH = np.append(rightH, 0)
            rightH = np.append(rightH, 1)

            leftH = leftH.reshape((3,3))
            rightH = rightH.reshape((3,3))

            leftHInverse = np.linalg.inv(leftH)
            rightHInverse = np.linalg.inv(rightH)

            mainPoints = Triangle(capB).getPoints()

            for car in mainPoints:
                x = np.append(car, 1)
                x = x.reshape(-1, 1)
                a = np.matmul(leftHInverse, x)
                b = np.matmul(rightHInverse, x)
                picture[int(car[1]), int(car[0])] = np.round((1-alpha)*splineLeft.ev(a[1], a[0]) + alpha * splineRight.ev(b[1], b[0]))

        return picture
