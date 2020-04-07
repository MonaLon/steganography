import os
from pathlib import Path
from detect import HiddenImage, HiddenText
import numpy as np
import imageio
import sys
import bitarray
from bitarray import util
import math
from pathlib import Path
from datetime import datetime
from PIL import Image

def make_found_dirs():
    'Make found_images and found_text directories'
    for _, dirnames, filenames in os.walk('./images'):
        for file in filenames:
            for dir in ['./found_text/', './found_images/']:
                os.remove(dir + file)
                os.mkdir(dir+file)

def get_int(self, bits, start=0, stop=8):
    try:
        bits = util.ba2int(bitarray.bitarray(bits[start:stop]))
    except:
        print("Could not convert bitstring to Int")
        return None
    return bits


def examine_channels():
    images = Path('./images')
    for _, dirnames, filenames in os.walk(images):
        for file in filenames:
            img = imageio.imread(images / file)
            height, width, alpha = img.shape

            # Look at each channel individually
            for channel in range(alpha):
                counter = 0
                header = []
                bits = []
                is_text = False
                for r in range(height):
                    for c in range(width):
                        if counter < 32:
                            header.append(str(img[r,c,channel] & 1))
                        elif counter == 32:
                            header = get_int("".join(header), 0, 32)

                            if header is not None and header < 9000:
                                is_text = True
                                bits.append(img[r,c,channel] & 1)

                        elif is_text:
                            bits.append(img[r,c,channel] & 1)

                        else:
                            break

                        counter += 1

                try:
                    with open (Path('./found_text/'+ file + '/channel' + channel + '.txt'), "w+") as f:
                        f.write(self.hidden_text)
                except:
                    print("Error. Saving text was not possible.")



if __name__ == '__main__':
    examine_channels()
