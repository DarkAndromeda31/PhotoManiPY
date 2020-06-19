"""
Module: edit_image for Photo ManiPY
Description:

Made by: Maximilian Rose
Created on 18/12/2019
IDE: PyCharm
"""

import math

from PIL import Image

import colors as c
import manage_image as mi


def shift_hsl(pic: Image, hue_shift: int, sat_shift: int, lum_shift: int) -> Image:
    """
    Function to change the hue, saturation and luminance of an image

    :param pic: The picture as an Image
    :param hue_shift: The amount to shift the hue by as an int
    :param sat_shift: The amount to shift the saturation by as an int
    :param lum_shift: The amount to shift the luminance by as an int

    :return: The edited picture as an Image
    """
    pixmap = pic.load()

    for i in range(pic.size[0]):  # for every col:
        for j in range(pic.size[1]):  # For every row
            color = c.rgb_hsl(pixmap[i, j])
            hsl_color = (color[0] + hue_shift, color[1] + sat_shift, color[2] + lum_shift)

            pixmap[i, j] = c.hsl_rgb(hsl_color)

    return pic


def crop(pic: Image, point1: tuple, point2: tuple) -> Image:
    """
    A function to crop an image when given two tuples that represent the coordinates of the corners.

    :param pic: The picture as an Image.
    :param point1: The top left point as a tuple in the form (x, y)
    :param point2: The bottom left point as a tuple in the form (x, y)
    :return: The new image object that has been generated
    """
    width = point2[0] - point1[0]
    hieght = point2[1] - point1[1]

    new_pic = Image.new('RGB', (width, hieght), color='black')

    pixmap = pic.load()
    new_pixmap = new_pic.load()

    for i in range(width):  # for every col:
        for j in range(hieght):  # For every row
            new_pixmap[i, j] = pixmap[i + point1[0], j + point1[1]]
            # print(new_pixmap[i, j])

    return new_pic


def resize(pic: Image, scale_factor: tuple) -> Image:
    """
    Function that resizes an image using the nearest neighbour algorithm.

    :param pic: The picture to be resized as an Image.
    :param scale_factor: The scale factor for the image as a tuple in the form (x_factor, y_factor)
    :return: The resized picture as an Image
    """
    width = math.floor(pic.size[0] * scale_factor[0])
    hieght = math.floor(pic.size[1] * scale_factor[1])

    new_pic = Image.new('RGB', (width, hieght), color='black')

    pixmap = pic.load()
    new_pixmap = new_pic.load()

    for i in range(width):  # for every col:
        for j in range(hieght):  # For every row
            new_pixmap[i, j] = pixmap[math.floor(i / scale_factor[0]), math.floor(j / scale_factor[1])]

    return new_pic


def subpixel_conversion(pic: Image) -> Image:
    """
    Function that converts from an rgb image to a rgb image that imitates the way that a LCD screen uses subpixels
    to display things.

    :param pic: The image to convert as an Image
    :return: The new image as an Image
    """
    width = pic.size[0] * 3
    hieght = pic.size[1] * 3

    new_pic = Image.new('RGB', (width, hieght), color='black')

    pixmap = pic.load()
    new_pixmap = new_pic.load()

    for i in range(pic.size[0]):  # for every col of the original image
        for j in range(pic.size[1]):  # For every row of the original image
            real_x = i * 3
            real_y = j * 3
            color = pixmap[i, j]

            for k in range(3):  # for every color
                for l in range(3):  # for every pixel of color
                    # if color == (255, 255, 255, 255):
                    #     new_pixmap[real_x + k, real_y + l] = (255, 255, 255)
                    if k == 0:
                        new_pixmap[real_x + k, real_y + l] = (color[0], 0, 0)
                    elif k == 1:
                        new_pixmap[real_x + k, real_y + l] = (0, color[1], 0)
                    elif k == 2:
                        new_pixmap[real_x + k, real_y + l] = (0, 0, color[2])

    return new_pic


if __name__ == '__main__':
    cur_image = mi.open_image("C:\\Users\\DarkA\\Desktop\\Capture.PNG")
    # shift_hsl(cur_image, 0, 10, 0)
    # crop(cur_image, (0, 0), (75, 100))
    # cur_image = resize(cur_image, (1.0, 1.0))

    cur_image = subpixel_conversion(cur_image)
    cur_image.show()
