"""
Module: colors for Photo ManiPY
Description: 

Made by: Maximilian Rose
Created on 18/12/2019
IDE: PyCharm
"""

from colorsys import hls_to_rgb, rgb_to_hls


def rgb_hsl(color):
    r, g, b = color
    r, g, b = [x / 255.0 for x in (r, g, b)]

    h, l, s = rgb_to_hls(r, g, b)

    h *= 360
    s *= 100
    l *= 100

    return (round(h), round(s), round(l))


def hsl_rgb(color):
    h, s, l = color
    h /= 360
    s /= 100
    l /= 100

    r, g, b = hls_to_rgb(h, l, s)

    return tuple(round(x * 255.0) for x in (r, g, b))


if __name__ == '__main__':
    color = (192, 64, 1)
    newcolor = rgb_hsl(color)
    newercolor = hsl_rgb(newcolor)
    print(newcolor)
    print(newercolor)
