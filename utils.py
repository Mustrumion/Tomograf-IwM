# -*- coding: utf-8 -*-

# _1 - początek, _2 - koniec
def bresenham(x1, y1, x2, y2):
    d = dx = dy = ai = bi = xi = yi = 0
    x = x1; y = y1
    # x1 zawsze większe niż x2?
    if x1 < x2:
        xi = 1
        dx = x2 - x1
    else:
        xi = -1
        dx = x1 - x2

    if y1 < y2:
        yi = 1
        dy = y2 - y1
    else:
        yi = -1
        dy = y1 - y2

    pixels = [(x, y)]

    # oś wiodąca OX
    if dx > dy:
        ai = (dy - dx) * 2
        bi = dy * 2
        d = bi - dx
        while x != x2:
            if d >= 0:
                x += xi
                y += yi
                d += ai
            else:
                d += bi
                x += xi

            pixels.append((x, y))

    # oś wiodąca OY
    else:
        ai = (dx - dy) * 2
        bi = dx * 2
        d = bi - dy
        while y != y2:
            if d >= 0:
                x += xi
                y += yi
                d += ai
            else:
                d += bi
                y += yi

            pixels.append((x, y))

    return pixels

if __name__ == '__main__':
    pixels = bresenham(20, 10, -20, -5)
    for p in pixels:
        print p
