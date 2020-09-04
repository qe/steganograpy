#!/usr/bin/env python

"""Generates an image with a concealed message within its pixel data.
"""

# Import libraries and modules
import numpy as np
from math import sqrt, ceil
from PIL import Image


# @message is a string
# @filename is a
def create_img(message, filename):
    '''
    Hello
    Will not work for a perfectly green image?
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


# @message is string of text
def dispense_bits(message):
    # For every character in the message
    # (e.g. for the first character in the message "Hello World", it will give the unicode value of "H" which is 72)
    for char in message:
        # Assigns the variable 'unicode_value' with the
        unicode_value: int = ord()
