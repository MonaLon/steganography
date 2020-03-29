import numpy as np
import imageio
import sys
import bitarray
from bitarray import util
import math
from pathlib import Path

def get_bits(path, num_bits):
    '''
    Reads in image at <path> and adds <num_bits> least significant bits (at each
    color channel) to a bytestring.
    '''
    # Read in image
    img = imageio.imread(path)

    # Calculate dimensions
    height, width, _ = img.shape
    print('height:', height, 'width:', width)

    # Initialize loop variables
    bits = []
    count = 0
    # Loop over dimensions of image
    for r in range(height):
        for c in range(width):
            # Grab the first <num_bits>
            if count < num_bits:
               bits.append(str(img[r,c,0] & 1))
               bits.append(str(img[r,c,1] & 1))
               bits.append(str(img[r,c,2] & 1))
               count += 1
            else:
                break

    print("extracted {0} bits from image.\n".format(count))
    return "".join(bits)

def get_chars(binary):
    '''
    Converts a bytestring to an ASCII string.
    '''
    text = bitarray.bitarray(binary).tobytes().decode('unicode_escape')
    print('binary of length {0} contained:\n{1}\n'.format(len(binary), text))
    return text

def get_dimensions(binary):
    first = binary[:32]
    second = binary[32:64]
    dim = (util.ba2int(bitarray.bitarray(first)), util.ba2int(bitarray.bitarray(second)))
    return dim


def get_img(binary, dimensions, path=Path('./found_images/found.jpg')):
    '''
    Convets a bytestring to an image and saves it to <path>.
    Use dimensions to extract the image
    '''
    # Calculate number of pixels in given bytestring
    pixels = int( math.sqrt( (len(binary) / (3*8)) ) )

    # Create an output image np array of appropriate size
    w, h = pixels, pixels
    hidden_img = np.zeros((h, w, 3), dtype=np.uint8)


    # Initialize loop counters
    counter = 0
    r = 0
    c = 0
    # Loop through output image, filling out pixel values
    while r < w:
        while c < h and counter < len(binary):
            # Index into the bytestring appropriately
            # and update output image

            # First 8 bits for the first color channel
            hidden_img[r, c, 0] = string_to_arr(binary[counter:counter+8])
            counter += 8
            hidden_img[r, c, 1] = string_to_arr(binary[counter:counter+8])
            counter += 8
            hidden_img[r, c, 2] = string_to_arr(binary[counter:counter+8])
            counter += 8
            # Manage inner loop counters
            c += 1
        # Manage outer loop counters
        r += 1

    print('{0} * {0} image created from bytestring of length {1} at {2}\n'.format(pixels, len(binary), path))
    imageio.imwrite(path, hidden_img)

    return hidden_img

def string_to_arr(string):
    list = [int(char) for char in string]
    return np.array(list)

if __name__ == "__main__":
    binary = get_bits(Path('./samples/hide_text.png'), 1528)
    text = get_chars(binary)

    binary = get_bits(Path('./samples/hide_image.png'), 1528)
    text = get_chars(binary)
    dimensions = get_dimensions(binary)
    img = get_img(binary, dimensions)
