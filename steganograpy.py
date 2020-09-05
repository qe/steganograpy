#!/usr/bin/env python

"""Generates an image with a concealed message within its pixel data.
"""

# Import libraries and modules
import numpy as np
from math import sqrt, ceil
from PIL import Image


# ENCODING
def create_img(message, filename):
    '''

    :param message:
    :param filename:
    :return:
    '''
    # Determine the minimum pixel size of the image needed to encode the message (based on message length)
    # Every character in message requires 8-bits
    bits_message = len(message) * 8
    # Calculate the minimum pixel side size for the image (square) given the minimum message length above
    img_side = ceil(sqrt(bits_message))
    # Use NumPy to create an array of numbers for the pixels, with 3 being for the RGB values of the image
    # Set the data type to 8-bit unsigned integers, which has a range of 0 to 255
    pixels = np.zeros([img_side, img_side, 3], dtype=np.uint8)
    # Set the starting image pixels entirely to green (i.e. R=0, G=255, B=0)
    pixels[:,:] = [0, 255, 0]
    # Enumerate gives both the index number and the bit value (binary digit) itself
    # The for loop iterates through the bits of the message
    for index, bit in enumerate(dispense_bits(message)):
        row = index // img_side
        col = index % img_side
        red_value = pixels[row, col][0]
        # Turn it off with a bit-wise 'and operation' with a bit-mask with a negation
        pixels[row, col][0] |= red_value & ~1 | bit
    # Now use the Image Library to generate an image from the pixels
    img = Image.fromarray(pixels)
    # Save the image
    img.save(filename)
    # Close the image
    img.close()


def dispense_bits(message):
    '''

    :param message:
    :return:
    '''
    # For every character in the message
    # (e.g. for the first character in the message "Hello World", it will give the unicode value of "H" which is 72)
    for char in message:
        # Assigns the variable 'unicode_value' with the
        unicode_value: int = ord(char)
        # Generates list of powers to use with 2 to map 2^7 (i.e. 128) to 0
        for power in range(7,-1,-1):
            # Yield generates the binary bits (TEMPORARY)
            # Yields the binary value of 1 if the unicode value matches with 2^ power value of the current iteration
            # Yields the binary value of 0 if it does not match
            yield 1 if unicode_value & 2 ** power else 0


# DECODING
def dispense_chars(bits):
    '''


    :param bits:
    :return:
    '''
    byte = 0
    for index, bit in enumerate(bits):
        power = 7-index % 8
        if bit:
            byte |= 2** power
        # At the end of each 8 bits (when the power goes down to zero)
        if power == 0:
            # Gives the respective unicode value, given the byte
            char: str = chr(byte)
            if not char.isprintable() and char != '\n':
                return
            yield char
            byte = 0


def decode_img(filename):
    '''

    :param filename:
    :return:
    '''
    img = Image.open(filename)
    # Extract red values from image and hand data to dispense_chars() function
    decoded = ''.join(dispense_chars(img.getdata(band=0)))
    img.close()
    return decoded
