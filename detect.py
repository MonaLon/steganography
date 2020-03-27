import numpy as np
import imageio
import sys
import bitarray
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

def get_img(binary, path=Path('./found_images/found.jpg')):
    '''
    Convets a bytestring to an image and saves it to <path>.
    '''
    # Calculate number of pixels in given bytestring
    pixels = int( math.sqrt( (len(binary) / 3) ) )

    # Create an output image np array of appropriate size
    w, h = pixels, pixels
    hidden_img = np.zeros((h, w, 3), dtype=np.uint8)

    # Initialize loop counters
    counter = 0
    r = 0
    c = 0
    # Loop through output image, filling out pixel values
    while r < w:
        while c < h:
            # Index into the bytestring appropriately
            # and update output image
            hidden_img[r, c, 0] = int(binary[counter]) & 1
            hidden_img[r, c, 1] = int(binary[counter + 1]) & 1
            hidden_img[r, c, 2] = int(binary[counter + 2]) & 1

            # Manage inner loop counters
            counter += 3
            c += 1
        # Manage outer loop counters
        r += 1

    print('{0} * {0} image created from bytestring of length {1} at {2}\n'.format(pixels, len(binary), path))
    imageio.imwrite(path, hidden_img)

    return hidden_img

if __name__ == "__main__":
    binary = get_bits(Path('./samples/hide_text.png'), 1528)
    text = get_chars(binary)

    header_binary = get_bits(Path('./samples/hide_image.png'), 64)
    text = get_chars(header_binary)

    binary = get_bits(Path('./samples/hide_image.png'), 1528)
    img = get_img(binary)
