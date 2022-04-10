"""
Module: codec for Photo ManiPY
Description: Module that reads or writes an image to .maxpg file format.

Made by: Maximilian Rose
Created on 30/01/2020
IDE: PyCharm
"""

from time import time

from PIL import Image

import manage_image as mi


def generate_body(pic: Image) -> bytes:
    """
    Function to concatenate the color values of every pixel in an image.

    :param pic: The picture as an Image
    :return: The concatenated list of integers
    """
    pixelmap = pic.load()

    pixel_list = []
    for i in range(pic.size[0]):  # for every col:
        for j in range(pic.size[1]):  # For every row
            pixel_list.append(pixelmap[i, j][0])
            pixel_list.append(pixelmap[i, j][1])
            pixel_list.append(pixelmap[i, j][2])

    pixel_list = bytes(pixel_list)

    return pixel_list


def generate_header(pic: Image) -> bytes:
    """
    Function to generate a binary header for a picture given the picture.

    :param pic: The picture as an Image.
    :return: The Header as binary bytes
    """
    header_length = 10  # 1 byte int
    width = pic.size[0]  # 4 byte int
    height = pic.size[1]  # 4 byte int
    date_created = int(time())  # 6 byte int
    bit_depth = 24  # 1 byte int

    header = [
        header_length.to_bytes(1, byteorder='big'),
        width.to_bytes(4, byteorder='big'),
        height.to_bytes(4, byteorder='big'),
        # date_created.to_bytes(6, byteorder='big'),
        bit_depth.to_bytes(1, byteorder='big'),
    ]

    header = b''.join(header)

    print(header)

    return header


def encode_image(pic: Image) -> bytes:
    """
    A function to encode an image into a MAXPG file format.

    :param pic: The picture as an Image.
    :return: The encoded picture as bytes.
    """
    header = generate_header(pic)
    body = generate_body(pic)

    binary = b''.join([header, body])

    return binary


def decode_body(binary: bytes, width: int, height: int, bit_depth: int) -> Image:
    """
    Decode the body of a MAXPG file, given the header data.

    :param binary: Body of the file, as binary in the form of Bytes
    :param width: The width of the image as an int
    :param height: The height of the image as an int
    :param bit_depth: The bit depth of the image as an int
    :return: The picture as an Image
    """
    pixel_data = []
    for byte in binary:
        pixel_data.append(byte)

    pic = Image.new('RGB', (width, height), color='black')
    pixmap = pic.load()

    counter = 0
    for i in range(width):  # for every col:
        for j in range(height):  # For every row
            pixmap[i, j] = (pixel_data[counter], pixel_data[counter + 1], pixel_data[counter + 2])
            counter += 3

    return pic


def decode_image(filename: str) -> Image:
    """
    A function to convert from a .maxpg file to a image

    :param filename: The file address of the picture.
    :return: The decoded image.
    """
    with open(filename, "rb") as f:
        binary = f.read()

    padding = binary[0]

    width = int.from_bytes(binary[1:5], byteorder='big')
    height = int.from_bytes(binary[6:9], byteorder='big')
    bit_depth = int.from_bytes(binary[9:10], byteorder='big')

    body = binary[padding:]

    pic = decode_body(body, width, height, bit_depth)
    pic.show()

    print("Decoded Image")

    return pic


def save_as_codec(pic: Image, filename: str) -> str:
    """
    A function to save a picture to a filename.

    :param pic: The picture as a Image.
    :param filename: The filename as a string *without* the file extension.
    :return The filename with extension.
    """
    binary = encode_image(pic)

    with open(filename, "wb+") as f:
        f.write(binary)

    print("Exported Image")

    return filename


if __name__ == '__main__':
    cur_image = mi.open_image("RGB_24bits_palette_sample_image.jpg")
    print(generate_header(cur_image))
    # encoded = encode_image(cur_image)
    # save_as_codec(cur_image, "bank.maxpg")
    # mi.save_image(decode_image(encoded), "codec.jpg")
    # datetime.fromtimestamp(time.time()).strftime('%c')

    # cur_image = decode_image("first_text.maxpg")
    # cur_image = decode_image("first_text.maxpg")
