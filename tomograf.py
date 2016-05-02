# -*- coding: utf-8 -*-
import numpy as np
import math
from skimage import data
from skimage.color import rgb2gray
from matplotlib import pyplot as plt
import sys

import utils


def main():
    deadangle = 0.4 * math.pi
    npoints = 50
    nrays = 50
    if len(sys.argv) > 1:
        filename = "images/" + sys.argv[1]
    else:
        filename = "images/image.bmp"

    output = np.zeros((npoints, nrays))

    image = rgb2gray(data.imread(filename))
    width = len(image[0])
    height = len(image)
    radius = math.ceil(((width**2+height**2)**0.5)/2) #obliczanie średnicy za pomocą twierdzenia Pitagorasa

    newwidth = newheight = 2*radius + 2  #ustalenie nowej wielkości obrazu
    if not width % 2 == 0: #sprawdzenie parzystości pikseli (aby środek obrazu pozostał na środku)
        newwidth += 1
    if not height % 2 == 0:
        newheight += 1

    #tworzenie nowego obrazu i kopiowanie starego do środka
    newimage = np.zeros((newheight, newwidth))
    xstart = (newwidth-width) / 2
    xend = xstart + width
    ystart = (newheight-height) / 2
    yend = ystart + height
    newimage[ystart:yend, xstart:xend] = image

    ax1 = plt.subplot(2, 1, 1)
    ax1.imshow(newimage, cmap='Greys_r', interpolation='none')

    # środek okręgu
    cirx = (newwidth-1) / 2
    ciry = (newheight-1) / 2
    # wrzucenie okregu do plota
    circle1 = plt.Circle((cirx, ciry), radius, color='r', fill=False)
    ax1.add_artist(circle1)

    points = np.zeros((npoints, 3)) #x, y, kąt stycznej do osi X+

    step = 2 * math.pi / npoints
    for point in xrange(npoints):
        points[point, 0] = cirx + radius * math.cos(step * point)
        points[point, 1] = ciry + radius * math.sin(step * point)
        points[point, 2] = step * point

    ax1.plot(points[:, 1], points[:, 0], 'ro')
    ax1.plot(points[0, 1], points[0, 0], 'bs')
    ax1.plot(points[1, 1], points[1, 0], 'gs')

    # angleStep = (math.pi - 2 * deadangle) / nrays
    # for pointNumber, smth in enumerate(points):
    #     for ray in xrange(nrays):
    #         angle = smth[2] + deadangle + angleStep * ray
    #         angle = angle % (2 * math.pi)
    #         #if ray==2: print angle
    #         output[pointNumber, ray] = recCountPixelSum(smth[0], smth[1], angle, newimage)
    #         #print deadangle + (math.pi - 2 * deadangle)/nrays*ray

    # Bresenham
    for pointNumber, pointerino in enumerate(points):
        for ray in xrange(nrays):
            angle = pointerino[2] + deadangle + ((2*math.pi - 2*deadangle) * float(ray)/nrays)
            # angle = smth[2] + deadangle + (math.pi - 2*deadangle) * float(ray)/nrays
            # angle = angle % (2 * math.pi)
            x2 = cirx + radius * math.cos(angle)
            y2 = ciry + radius * math.sin(angle)
            pixels = utils.bresenham(int(round(pointerino[0])), int(round(pointerino[1])), int(round(x2)), int(round(y2)))

            weight = 0.0
            if math.sin(angle%(math.pi/2)) > math.cos(angle%(math.pi/2)):
                weight = 1 / math.sin(angle%(math.pi/2))
            else:
                weight = 1 / math.cos(angle%(math.pi/2))

            output[pointNumber, ray] = sum([newimage[i] for i in pixels]) * weight

    maxp = output.max(axis=1)
    i = 0
    if all(maxp > 0):
        for pixel in np.nditer(output, op_flags=['readwrite']):
            pixel[...] = pixel / maxp[i]
            i = (i+1) % nrays

    ax3 = plt.subplot(2, 2, 3)
    ax3.imshow(output, cmap='Greys_r', interpolation='none')

    # Rekonstrukcja
    reconstructedImg = np.zeros((newheight, newwidth))

    for pointNumber, pointerino in enumerate(points):
        for ray in xrange(nrays):
            sample = output[pointNumber, ray]
            if sample > 0:
                angle = pointerino[2] + deadangle + ((2*math.pi - 2*deadangle) * float(ray)/nrays)
                x2 = cirx + radius * math.cos(angle)
                y2 = ciry + radius * math.sin(angle)
                pixels = utils.bresenham(int(round(pointerino[0])), int(round(pointerino[1])), int(round(x2)), int(round(y2)))
                rows, cols = [], []
                for p in pixels:
                    rows.append(p[0])
                    cols.append(p[1])

                reconstructedImg[rows, cols] += sample

    ax4 = plt.subplot(2, 2, 4)
    ax4.imshow(reconstructedImg, cmap='Greys_r', interpolation='none')

    plt.show()


if __name__ == '__main__':
    main()
