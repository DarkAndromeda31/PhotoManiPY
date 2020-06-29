"""
Module: manage_image for Photo ManiPY
Description: Module that saves and opens images

Made by: Maximilian Rose
Created on 18/12/2019
IDE: PyCharm
"""

from PIL import Image


def open_image(filename: str) -> Image:
    """
    A function to open an image from a given filepath and return a PIL image object

    :param filename: THe filename / filepath of the image
    :return: The image as a PIL image object
    """

    pic = Image.open(filename)

    return pic


def save_image(pic: Image, filename):
    """
    Really simple function that I don't know why I even have, saves an image from the given Image object and a filename

    :param pic: The picture as an Image
    :param filename: The filename (including file address) to save as. As an string
    """
    pic.save(filename)


if __name__ == '__main__':
    # pics = open_image("RGB_24bits_palette_sample_image.jpg")

    colors = [128, 128, 128]
    print(bytearray(colors))
