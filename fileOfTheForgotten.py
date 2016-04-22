import math

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
