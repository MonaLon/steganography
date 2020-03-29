import numpy as np
import imageio
import sys
import bitarray
from bitarray import util
import math
from pathlib import Path

def get_bits(path):
    '''
    Reads in image at <path> and adds <num_bits> least significant bits (at each
    color channel) to a bytestring.
    '''
    # Read in image
    img = imageio.imread(path)

    # Calculate dimensions
    height, width, _ = img.shape

    num_bits = height * width

    print('height:', height, 'width:', width, 'number of pixels:', num_bits)

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

def get_int(binary):
    '''
    Converts <binary> to int
    '''
    return util.ba2int(bitarray.bitarray(binary))

def get_chars(binary, length):
    '''
    Converts a bytestring to an ASCII string.
    '''
    text = bitarray.bitarray(binary[:length]).tobytes().decode('unicode_escape')
    print('binary of length {0} contained:\n{1}\n'.format(len(binary), text))
    return text

def get_dimensions(binary):
    '''
    Looks at the first 64 bits of <binary> for 2 unsigned intergers.
    '''
    first = binary[:32]
    second = binary[32:64]
    dim = (get_int(first), get_int(second))
    return dim

def get_img(binary, dimensions, path=Path('./found_images/found.jpg')):
    '''
    Convets a bytestring to an image and saves it to <path>.
    Use dimensions to extract the image
    '''

    # Create an output image np array of appropriate size
    w, h = dimensions[0], dimensions[1]
    hidden_img = np.zeros((h, w, 3), dtype=np.uint8)

    # Initialize loop counters
    counter = 0
    r = 0
    c = 0
    pixels = 0
    # Loop through output image, filling out pixel values
    while r < w:
        while c < h:
            # Index into the bytestring appropriately
            # and update output image

            first_c = binary[counter:counter+8]
            counter += 8
            second_c = binary[counter:counter+8]
            counter += 8
            third_c = binary[counter:counter+8]
            counter += 8

            # First 8 bits for the first color channel
            hidden_img[c, r, 0] = get_int(first_c)
            hidden_img[c, r, 1] = get_int(second_c)
            hidden_img[c, r, 2] = get_int(third_c)

            pixels += 1

            # Manage inner loop counters
            c += 1
        # Manage outer loop counters
        r += 1
        c = 0

    print('{0} * {1} image created from bytestring of length {2} at {3}\n'.format(w, h, counter, path))
    imageio.imwrite(path, hidden_img)

    return hidden_img


if __name__ == "__main__":
    binary = get_bits(Path('./samples/hide_text.png'))
    text = get_chars(binary, 4580)

    binary = get_bits(Path('./samples/hide_image.png'))
    dimensions = get_dimensions(binary)
    img = get_img(binary[64:], dimensions) # No header
