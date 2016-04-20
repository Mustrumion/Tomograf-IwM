# -*- coding: utf-8 -*-
import numpy as np
import math
from skimage import data
from skimage.color import rgb2gray
from matplotlib import pyplot as plt
import sys

'''this function crawls (yeah, crawls, not walks) along the line checking which
side of pixel is crossed to determine next pixel, adding their colours on the way'''

def recCountPixelSum(startx, starty, angle, photo): #works, looks like shit though
    #print startx, starty, angle
    tan = abs( math.tan(angle) )
    if angle < 0.5*math.pi:

        if startx > len(photo[0])-1 or starty < 0:
            return 0

        xleft = (startx+0.5) % 1
        if xleft == 0: xleft = 1
        yleft = 1-(starty+0.5) % 1

        xleftscaled = xleft * tan

        if (xleftscaled > yleft): #top side is crossed first
            newstarty = starty - yleft
            xleft = yleft / tan
            newstartx = startx + xleft
            leng = (xleft**2 + yleft**2)**0.5
            return photo[math.ceil(starty-0.5),math.floor(startx+0.5)]*leng\
                    +recCountPixelSum(newstartx, newstarty, angle, photo)
        else:
            yleft = xleft * tan
            newstarty = starty - yleft
            newstartx = startx + xleft
            leng = (xleft**2 + yleft**2)**0.5
            return photo[math.ceil(starty-0.5),math.floor(startx+0.5)]*leng\
                    +recCountPixelSum(newstartx, newstarty, angle, photo)

    if angle == 0.5*math.pi:
        '''newstartx=startx
        newstarty=math.ceil(starty-0.5)-0.5
        return photo[math.floor(startx+0.5),math.floor(starty+0.5)]*(starty-newstarty)\
                +recCountPixelSum(newstartx, newstarty, angle, photo)'''
        return 0

    if angle > 0.5*math.pi and angle <= math.pi:
        if (startx < 0 or starty < 0):
            return 0

        xleft = 1-(startx+0.5) % 1
        yleft = 1-(starty+0.5) % 1

        xleftscaled = xleft * tan

        if (xleftscaled > yleft): #top side is crossed first
            xleft = yleft / tan
            newstarty = starty - yleft
            newstartx = startx - xleft
            leng = (xleft**2 + yleft**2)**0.5
            return photo[math.ceil(starty-0.5),math.ceil(startx-0.5)]*leng\
                    +recCountPixelSum(newstartx, newstarty, angle, photo)
        else:
            yleft = xleft * tan
            newstarty = starty - yleft
            newstartx = startx - xleft
            leng = (xleft**2 + yleft**2)**0.5
            return photo[math.ceil(starty-0.5),math.ceil(startx-0.5)]*leng\
                    +recCountPixelSum(newstartx, newstarty, angle, photo)

    if angle > math.pi and angle < 1.5 * math.pi:
        if (startx < 0 or starty > len(photo)-1):
            return 0

        yleft = (starty+0.5) % 1
        if yleft == 0: yleft = 1
        xleft = 1-(startx+0.5) % 1

        xleftscaled = xleft * tan

        if (xleftscaled > yleft): #top side is crossed first
            newstarty = starty + yleft
            xleft = yleft / tan
            newstartx = startx - xleft
            leng = (xleft**2 + yleft**2)**0.5
            return photo[math.floor(starty+0.5),math.ceil(startx-0.5)]*leng\
                    +recCountPixelSum(newstartx, newstarty, angle, photo)
        else:
            yleft = xleft * tan
            newstarty = starty + yleft
            newstartx = startx - xleft
            leng = (xleft**2 + yleft**2)**0.5
            return photo[math.floor(starty+0.5),math.ceil(startx-0.5)]*leng\
                    +recCountPixelSum(newstartx, newstarty, angle, photo)

    if angle > math.pi * 1.5:

        if (startx > len(photo[0])-1 or starty > len(photo)-1):
            return 0

        yleft = (starty+0.5) % 1
        if yleft == 0: yleft = 1
        xleft = (startx+0.5) % 1
        if xleft == 0: xleft = 1

        xleftscaled = xleft * tan

        if xleftscaled > yleft: #top side is crossed first
            newstarty = starty + yleft
            xleft = yleft / tan
            newstartx = startx + xleft
            leng = (xleft**2 + yleft**2)**0.5
            return photo[math.floor(starty+0.5),math.floor(startx+0.5)]*leng\
                    +recCountPixelSum(newstartx, newstarty, angle, photo)
        else:
            yleft = xleft * tan
            newstarty = starty + yleft
            newstartx = startx + xleft
            leng = (xleft**2 + yleft**2)**0.5
            return photo[math.floor(starty+0.5),math.floor(startx+0.5)]*leng\
                    +recCountPixelSum(newstartx, newstarty, angle, photo)

    return 0



def main():
    deadangle = 0.2 * math.pi
    npoints = 50
    nrays = 50
    if len(sys.argv) > 1:
        filename = "images/" + sys.argv[1]
    else:
        filename = "images/image.bmp"

    output = np.zeros((npoints,nrays))

    image = rgb2gray(data.imread(filename))
    width = len(image[0])
    height = len(image)
    radius = math.ceil(((width**2+height**2)**0.5)/2) #obliczanie średnicy za pomocą twierdzenia Pitagorasa

    newwidth = newheight = 2*radius + 2  #ustalenie nowej wielkości obrazu
    if not width % 2 == 0: #sprawdzenie parzystości pikseli (aby środek obrazu pozostał na środku)
        newwidth+=1
    if not height % 2 == 0:
        newheight+=1

    #tworzenie nowego obrazu i kopiowanie starego do środka
    newimage = np.zeros((newheight,newwidth))
    #print width, height
    #print newwidth, newheight
    xstart = (newwidth-width) / 2
    xend = xstart + width
    ystart = (newheight-height) / 2
    yend = ystart + height
    #print xstart,xend,ystart,yend
    newimage[ystart:yend,xstart:xend]=image

    f, (ax1, ax2) = plt.subplots(1, 2)

    ax1.imshow(newimage,cmap='Greys_r',interpolation='none')

    cirx = ((newheight-1)/2) #środek okręgu
    ciry = ((newwidth-1)/2)
    circle1=plt.Circle((ciry,cirx),radius,color='r',fill=False)  #wrzucenie okregu do plota
    ax1.add_artist(circle1)


    points = np.zeros((npoints,3)) #x,y,kąt stycznej do osi X+

    for point in xrange(npoints):
        points[point,0] = cirx+radius * math.cos(2 * math.pi / npoints * point)
        points[point,1] = ciry+radius * math.sin(2 * math.pi / npoints * point)
        points[point,2] = 2 * math.pi / npoints * point

    #print points

    ax1.plot(points[:,1], points[:,0], 'ro')
    ax1.plot(points[0,1], points[0,0], 'bs')
    ax1.plot(points[1,1], points[1,0], 'gs')

    pointnumber = 0
    for smth in points:
        for ray in xrange(nrays):
            angle = smth[2] + deadangle + (math.pi - 2 * deadangle) / nrays*ray
            angle = angle % (2 * math.pi)
            #if ray==2: print angle
            output[pointnumber,ray] = recCountPixelSum(smth[1],smth[0],angle,newimage)
            #print deadangle + (math.pi - 2 * deadangle)/nrays*ray

        pointnumber+=1

    #print points

    maxp = output.max(axis=1)
    if all(maxp > 0):
        for line in output:
            for pixel in line:
                pixel/=maxp

    ax2.imshow(output,cmap='Greys_r',interpolation='none')

    plt.show()


if __name__ == '__main__':
    main()
