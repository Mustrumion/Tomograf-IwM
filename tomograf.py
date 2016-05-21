# -*- coding: utf-8 -*-
import numpy as np
import math
from skimage import data
from skimage.color import rgb2gray
from matplotlib import pyplot as plt
import argparse

import utils


class Tomograph:
    def __init__(self):
        # parse cmd line args
        parser = argparse.ArgumentParser()
        parser.add_argument('--points', '-p', default=100, type=int)
        parser.add_argument('--rays', '-r', default=100, type=int)
        parser.add_argument('--image', '-i', default='image.bmp')
        args = parser.parse_args()

        self.deadangle = 0.4 * math.pi
        self.npoints = args.points
        self.points = np.zeros((self.npoints, 3)) #x, y, kąt stycznej do osi X+
        self.nrays = args.rays
        self.filename = 'images/' + args.image
        self.cirx, self.ciry = 0, 0
        self.radius = 0
        self.extendedImage = []
        self.spectrum = np.zeros((self.npoints, self.nrays))
        self.reconstructedImage = []
        self.accuracy = 0.0

    def getLinePixels(self, angle, pointerino, ray):
        x2 = self.cirx + self.radius * math.cos(angle)
        y2 = self.ciry + self.radius * math.sin(angle)
        return utils.bresenham(int(round(pointerino[0])), int(round(pointerino[1])), int(round(x2)), int(round(y2)))

    def scan(self):
        for pointNumber, pointerino in enumerate(self.points):
            for ray in xrange(self.nrays):
                angle = pointerino[2] + self.deadangle + ((2*math.pi - 2*self.deadangle) * float(ray)/self.nrays)
                pixels = self.getLinePixels(angle, pointerino, ray)

                weight = 0.0
                if math.sin(angle%(math.pi/2)) > math.cos(angle%(math.pi/2)):
                    weight = 1 / math.sin(angle%(math.pi/2))
                else:
                    weight = 1 / math.cos(angle%(math.pi/2))

                self.spectrum[pointNumber, ray] = sum([self.extendedImage[i] for i in pixels]) * weight

        maxp = self.spectrum.max(axis=1)
        i = 0
        if all(maxp > 0):
            for pixel in np.nditer(self.spectrum, op_flags=['readwrite']):
                pixel[...] = pixel / maxp[i]
                i = (i+1) % self.nrays

    def reconstruct(self):
        self.reconstructedImage = np.zeros(self.extendedImage.shape)

        for pointNumber, pointerino in enumerate(self.points):
            for ray in xrange(self.nrays):
                sample = self.spectrum[pointNumber, ray]
                if sample > 0:
                    angle = pointerino[2] + self.deadangle + ((2*math.pi - 2*self.deadangle) * float(ray)/self.nrays)
                    pixels = self.getLinePixels(angle, pointerino, ray)
                    rows, cols = [], []
                    for p in pixels:
                        rows.append(p[0])
                        cols.append(p[1])

                    self.reconstructedImage[rows, cols] += sample

        self.reconstructedImage = self.reconstructedImage / np.amax(self.reconstructedImage)


    def simulate(self):
        image = rgb2gray(data.imread(self.filename))
        width = len(image[0])
        height = len(image)
        self.radius = math.ceil(((width**2+height**2)**0.5)/2) #obliczanie średnicy za pomocą twierdzenia Pitagorasa

        newwidth = newheight = 2*self.radius + 2  #ustalenie nowej wielkości obrazu
        if not width % 2 == 0: #sprawdzenie parzystości pikseli (aby środek obrazu pozostał na środku)
            newwidth += 1
        if not height % 2 == 0:
            newheight += 1

        #tworzenie nowego obrazu i kopiowanie starego do środka
        self.extendedImage = np.zeros((newheight, newwidth))
        xstart = (newwidth-width) / 2
        xend = xstart + width
        ystart = (newheight-height) / 2
        yend = ystart + height
        self.extendedImage[ystart:yend, xstart:xend] = image

        ax1 = plt.subplot(2, 2, 1)
        ax1.imshow(self.extendedImage, cmap='Greys_r', interpolation='none')

        # środek okręgu
        self.cirx = (newwidth-1) / 2
        self.ciry = (newheight-1) / 2
        # wrzucenie okregu do plota
        circle1 = plt.Circle((self.cirx, self.ciry), self.radius, color='r', fill=False)
        ax1.add_artist(circle1)

        step = 2 * math.pi / self.npoints
        for point in xrange(self.npoints):
            self.points[point, 0] = self.cirx + self.radius * math.cos(step * point)
            self.points[point, 1] = self.ciry + self.radius * math.sin(step * point)
            self.points[point, 2] = step * point

        ax1.plot(self.points[:, 1], self.points[:, 0], 'ro')
        ax1.plot(self.points[0, 1], self.points[0, 0], 'bs')
        ax1.plot(self.points[1, 1], self.points[1, 0], 'gs')

        # Skanowanie
        self.scan()
        ax2 = plt.subplot(2, 2, 2)
        ax2.imshow(self.spectrum, cmap='Greys_r', interpolation='none')

        # Rekonstrukcja
        self.reconstruct()
        ax3 = plt.subplot(2, 2, 3)
        ax3.imshow(self.reconstructedImage, cmap='Greys_r', interpolation='none')

        error = self.reconstructedImage - self.extendedImage
        ax4 = plt.subplot(2, 2, 4)
        ax4.imshow(error, cmap='Greys_r', interpolation='none')

        self.countAccuracy()

        plt.show()


    def countAccuracy(self):
        for lineOriginal, lineReconstructed in zip(self.extendedImage, self.reconstructedImage):
            for pixelOriginal, pixelReconstructed in zip(lineOriginal, lineReconstructed):
                self.accuracy += (pixelOriginal - pixelReconstructed) **2

        self.accuracy /= len(self.extendedImage)*len(self.extendedImage[0])
        print(self.accuracy)


if __name__ == '__main__':
    tomograph = Tomograph()
    tomograph.simulate()
