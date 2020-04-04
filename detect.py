import os
import numpy as np
import imageio
import sys
import bitarray
from bitarray import util
import math
from pathlib import Path
from datetime import datetime
from PIL import Image


class ImageBits(object):
    '''
    Class used to extract bits from an Image
    '''
    def __init__(self, path, bit_pattern='first', bits=None):
        '''
        EDIT THIS SO IT CAN WORK WITH OTHER BIT ENCODINGS (evens,
        odds, first two, first three, etc...)
        '''
        self.path = path
        self.img = imageio.imread(path)
        self.height, self.width, _ = self.img.shape
        self.bitlength = self.height * self.width

        if bits is None:
            # Initialize loop variables
            bits = []
            count = 0
            # Loop over dimensions of image
            for r in range(self.height):
                for c in range(self.width):
                    # Grab the first <num_bits>
                    if count < self.bitlength:
                       bits.append(str(self.img[r,c,0] & 1))
                       bits.append(str(self.img[r,c,1] & 1))
                       bits.append(str(self.img[r,c,2] & 1))
                       count += 1
                    else:
                        break

            self.bits = "".join(bits)
        else:
            self.bits = bits

    def get_bits(self):
        return self.bits

    def width(self):
        return self.width

    def height(self):
        return self.height

    def set_bits(self, bits):
        self.bits = bits

    def save_bits(self):
        with open (Path('./found_bits/' + os.path.basename(self.path) +  '/found' + datetime.now().strftime("%m:%d:%Y:%H:%M:%S") +'.txt'), "w+") as f:
            f.write(self.bits)

    def get_int(self, bits=None, start=0, stop=8):
        if bits is None:
            bits = self.bits
        return util.ba2int(bitarray.bitarray(bits[start:stop]))

class HiddenImage(ImageBits):
    '''
    Class used to detect and translate nested hidden images
    '''

    def __init__(self, path='./samples/hide_image.png', dimensions=(60, 80), bits=None):
        super().__init__(path, bits=bits)
        self.dimensions = dimensions
        self.hidden_img = None
        self.header()

    def __str__(self):
        if self.hidden_img is None:
            return "Hidden image as np.array:\n{0}".format(self.find())
        return "Hidden image as np.array:\n{0}".format(self.hidden_img)

    def header(self, first=0, second=32):
        '''
        Looks at the first 64 bits of <binary> for 2 unsigned intergers.
        '''
        first = self.bits[first:first+32]
        second = self.bits[second:second+32]
        self.dimensions = None
        try:
            self.dimensions = (self.get_int(first, 0, 32), self.get_int(second, 0, 32))
        except:
            "There was an error in reading in the dimensions"
        return self.dimensions

    def find(self, start=64, w=None, h=None, first=0, second=32):
        '''
        Convets a bytestring to an image and saves it to <path>.
        Use dimensions to extract the image
        '''
        if self.hidden_img is not None:
            return self.hidden_img

        # Create an output image np array of appropriate size
        if w is None:
            w = self.header(first, second)[0]
        if h is None:
            h = self.header(first, second)[1]

        # Start our search after the header
        binary = self.bits[start:]
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
                hidden_img[c, r, 0] = self.get_int(first_c)
                hidden_img[c, r, 1] = self.get_int(second_c)
                hidden_img[c, r, 2] = self.get_int(third_c)

                pixels += 1

                # Manage inner loop counters
                c += 1
            # Manage outer loop counters
            r += 1
            c = 0

        print('{0} * {1} image created from bytestring of length {2} at {3}\n'.format(w, h, counter, Path('./found_images/found'+ datetime.now().strftime("%m:%d:%Y:%H:%M:%S") +'.jpg')))
        self.hidden_img = hidden_img

        try:
            self.save()
        except:
            "This hidden image could not be turned into a imageio img"

        return hidden_img

    def rotate(self, degrees):
        if self.hidden_img is None:
            self.find()
        img = Image.fromarray(self.hidden_img)
        img = img.rotate(degrees)
        self.hidden_img = np.array(img)
        self.save()
        return self.hidden_img

    def save(self):
        if self.hidden_img is None:
            self.find()
        imageio.imwrite(Path('./found_images/found'+ datetime.now().strftime("%m:%d:%Y:%H:%M:%S") +'.jpg'), self.hidden_img)
        return True


class HiddenText(ImageBits):
    def __init__(self, path='./samples/hide_text.png', dimensions=(32, 4580), bits=None):
        super().__init__(path, bits=bits)
        self.dimensions = dimensions
        self.hidden_text = None
        self.header()

    def __str__(self):
        if self.hidden_text is None:
            return self.find()
        return self.hidden_text

    def header(self, start=0, stop=32):
        '''
        Converts <binary> to int
        '''
        self.dimensions=(32, util.ba2int(bitarray.bitarray(self.bits[start:stop])))
        return util.ba2int(bitarray.bitarray(self.bits[start:stop]))

    def find(self, start=None, stop=None):
        '''
        Finds hidden text in its image between <start> and <stop>
        '''
        if self.hidden_text is not None:
            return self.hidden_text
        if start is None: start = self.dimensions[0]
        if stop is None: stop = self.dimensions[1]

        text = None

        try:
            text = bitarray.bitarray(self.bits[start:stop]).tobytes().decode('unicode_escape')
            print('Text found in binary of length {0}:\n{1}'.format(self.bitlength, text))
            self.hidden_text = text
            self.save()
        except:
            'Text could not be decoded'
        return text

    def save(self):
        if self.hidden_text is None:
            self.find()
        with open (Path('./found_text/found'+ datetime.now().strftime("%m:%d:%Y:%H:%M:%S") +'.txt'), "w+") as f:
            f.write(self.hidden_text)
        return True

if __name__ == "__main__":
    # Usage
    hi = HiddenImage()
    print(hi)
    hi.rotate(270)

    ht = HiddenText()
    print(ht)
