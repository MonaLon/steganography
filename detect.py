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
    def __init__(self, path, bit_pattern=None, combine=None, bits=None, rotation=0, channel=None, swap=False, reversed=False, diagonal=False):

        '''
        EDIT THIS SO IT CAN WORK WITH OTHER BIT ENCODINGS (evens,
        odds, first two, first three, etc...)
        '''
        if bit_pattern is None:
            bit_pattern = input("Input 'first', 'second', 'third', etc.: ")
        if combine is None:
            combine = input("Input true or false for combining the bits extracted: ")
        self.path = path

        self.img = imageio.imread(path)
        if rotation != 0:
            self.img = self.rotate(rotation)
        self.height, self.width, _ = self.img.shape
        self.bitLength = self.height * self.width
        count = 0

        if bits is not None:
            self.bits = bits
            return

        # Initialize loop variables
        bits = []

        # Right to left or left to right
        if not reversed:
            start = 0
            stop = self.width
            step = 1
        else:
            start = self.width - 1
            stop = -1
            step = -1

        if (combine == 'true') and channel is None:
            for r in range(self.height):
                for c in range(start, stop, step):
                    if count < self.bitLength:
                        if (bit_pattern == 'first'):
                            fTup = self.first(r, c)
                            if swap:
                                fTup = list(fTup)
                                fTup.reverse()
                            for var in fTup:
                                bits.append(var)
                        if (bit_pattern == 'second'):
                            sTup = self.second(r, c)
                            fTup = self.first(r, c)
                            if swap:
                                fTup = list(fTup)
                                fTup.reverse()
                                sTup = list(sTup)
                                sTup.reverse()
                            i = 0
                            while i < 3:
                                bits.append(fTup[i])
                                bits.append(sTup[i])
                                i += 1
                        if (bit_pattern == 'third'):
                            tTup = self.third(r, c)
                            sTup = self.second(r, c)
                            fTup = self.first(r, c)
                            if swap:
                                fTup = list(fTup)
                                fTup.reverse()
                                sTup = list(sTup)
                                sTup.reverse()
                                tTup = list(tTup)
                                tTup.reverse()
                            i = 0
                            while i < 3:
                                bits.append(fTup[i])
                                bits.append(sTup[i])
                                bits.append(tTup[i])
                                i += 1
                        if (bit_pattern == 'fourth'):
                            foTup = self.fourth(r, c)
                            tTup = self.third(r, c)
                            sTup = self.second(r, c)
                            fTup = self.first(r, c)
                            if swap:
                                fTup = list(fTup)
                                fTup.reverse()
                                sTup = list(sTup)
                                sTup.reverse()
                                tTup = list(tTup)
                                tTup.reverse()
                                foTup = list(foTup)
                                foTup.reverse()
                            i = 0
                            while i < 3:
                                bits.append(fTup[i])
                                bits.append(sTup[i])
                                bits.append(tTup[i])
                                bits.append(foTup[i])
                                i += 1
                        if (bit_pattern == 'fifth'):
                            fiTup = self.fifth(r, c)
                            foTup = self.fourth(r, c)
                            tTup = self.third(r, c)
                            sTup = self.second(r, c)
                            fTup = self.first(r, c)
                            if swap:
                                fTup = list(fTup)
                                fTup.reverse()
                                sTup = list(sTup)
                                sTup.reverse()
                                tTup = list(tTup)
                                tTup.reverse()
                                foTup = list(foTup)
                                foTup.reverse()
                                fiTup = list(fiTup)
                                fiTup.reverse()
                            i = 0
                            while i < 3:
                                bits.append(fTup[i])
                                bits.append(sTup[i])
                                bits.append(tTup[i])
                                bits.append(foTup[i])
                                bits.append(fiTup[i])
                                i += 1
                        if (bit_pattern == 'sixth'):
                            siTup = self.sixth(r, c)
                            fiTup = self.fifth(r, c)
                            foTup = self.fourth(r, c)
                            tTup = self.third(r, c)
                            sTup = self.second(r, c)
                            fTup = self.first(r, c)
                            if swap:
                                fTup = list(fTup)
                                fTup.reverse()
                                sTup = list(sTup)
                                sTup.reverse()
                                tTup = list(tTup)
                                tTup.reverse()
                                foTup = list(foTup)
                                foTup.reverse()
                                siTup = list(siTup)
                                siTup.reverse()
                            i = 0
                            while i < 3:
                                bits.append(fTup[i])
                                bits.append(sTup[i])
                                bits.append(tTup[i])
                                bits.append(foTup[i])
                                bits.append(fiTup[i])
                                bits.append(siTup[i])
                                i += 1
                        if (bit_pattern == 'seventh'):
                            seTup = self.seventh(r, c)
                            siTup = self.sixth(r, c)
                            fiTup = self.fifth(r, c)
                            foTup = self.fourth(r, c)
                            tTup = self.third(r, c)
                            sTup = self.second(r, c)
                            fTup = self.first(r, c)
                            if swap:
                                fTup = list(fTup)
                                fTup.reverse()
                                sTup = list(sTup)
                                sTup.reverse()
                                tTup = list(tTup)
                                tTup.reverse()
                                foTup = list(foTup)
                                foTup.reverse()
                                siTup = list(siTup)
                                siTup.reverse()
                                seTup = list(seTup)
                                seTup.reverse()
                            i = 0
                            while i < 3:
                                bits.append(fTup[i])
                                bits.append(sTup[i])
                                bits.append(tTup[i])
                                bits.append(foTup[i])
                                bits.append(fiTup[i])
                                bits.append(siTup[i])
                                bits.append(seTup[i])
                                i += 1
                        if (bit_pattern == 'eighth'):
                            eiTup = self.eighth(r, c)
                            seTup = self.seventh(r, c)
                            siTup = self.sixth(r, c)
                            fiTup = self.fifth(r, c)
                            foTup = self.fourth(r, c)
                            tTup = self.third(r, c)
                            sTup = self.second(r, c)
                            fTup = self.first(r, c)
                            if swap:
                                fTup = list(fTup)
                                fTup.reverse()
                                sTup = list(sTup)
                                sTup.reverse()
                                tTup = list(tTup)
                                tTup.reverse()
                                foTup = list(foTup)
                                foTup.reverse()
                                siTup = list(siTup)
                                siTup.reverse()
                                seTup = list(seTup)
                                seTup.reverse()
                                eiTup = list(eiTup)
                                eiTup.reverse()
                            i = 0
                            while i < 3:
                                bits.append(fTup[i])
                                bits.append(sTup[i])
                                bits.append(tTup[i])
                                bits.append(foTup[i])
                                bits.append(fiTup[i])
                                bits.append(siTup[i])
                                bits.append(seTup[i])
                                bits.append(eiTup[i])
                                i += 1
                        count += 1
            self.bits = "".join(bits)
        elif channel is not None:
            for r in range(self.height):
                for c in range(start, stop, step):
                    fTup = self.first(r, c)
                    sTup = self.second(r, c)
                    tTup = self.third(r, c)
                    foTup = self.fourth(r, c)
                    fiTup = self.fifth(r, c)
                    siTup = self.sixth(r, c)
                    seTup = self.seventh(r, c)
                    eiTup = self.eighth(r, c)

                    for tup in [fTup, sTup, tTup, foTup, fiTup, siTup, seTup, eiTup]:
                        bits.append(tup[channel])

            self.bits = "".join(bits)           
        else:
            for r in range(self.height):
                for c in range(start, stop, step):
                    if count < self.bitLength:
                        if (bit_pattern == 'first'):
                            fTup = self.first(r, c)
                            if swap:
                                fTup = list(fTup)
                                fTup.reverse()
                            if diagonal:
                                if r == c:
                                    for var in fTup:
                                        bits.append(var)
                                    break
                            for var in fTup:
                                bits.append(var)
                        elif (bit_pattern == 'second'):
                            sTup = self.second(r, c)
                            if swap:
                                sTup = list(sTup)
                                sTup.reverse()
                            if diagonal:
                                if r == c:
                                    for var in sTup:
                                        bits.append(var)
                                    break
                            for var in sTup:
                                bits.append(var)
                        elif (bit_pattern == 'third'):
                            tTup = self.third(r, c)
                            if swap:
                                tTup = list(tTup)
                                tTup.reverse()
                            if diagonal:
                                if r == c:
                                    for var in tTup:
                                        bits.append(var)
                                    break
                            for var in tTup:
                                bits.append(var)
                        elif (bit_pattern == 'fourth'):
                            foTup = self.fourth(r, c)
                            if swap:
                                foTup = list(foTup)
                                foTup.reverse()
                            if diagonal:
                                if r == c:
                                    for var in foTup:
                                        bits.append(var)
                                    break
                            for var in foTup:
                                bits.append(var)
                        elif (bit_pattern == 'fifth'):
                            fiTup = self.fifth(r, c)
                            if swap:
                                fiTup = list(fiTup)
                                fiTup.reverse()
                            if diagonal:
                                if r == c:
                                    for var in fiTup:
                                        bits.append(var)
                                    break
                            for var in fiTup:
                                bits.append(var)
                        elif (bit_pattern == 'sixth'):
                            siTup = self.sixth(r, c)
                            if swap:
                                siTup = list(siTup)
                                siTup.reverse()
                            if diagonal:
                                if r == c:
                                    for var in siTup:
                                        bits.append(var)
                                    break
                            for var in siTup:
                                bits.append(var)
                        elif (bit_pattern == 'seventh'):
                            seTup = self.seventh(r, c)
                            if swap:
                                seTup = list(seTup)
                                seTup.reverse()
                            if diagonal:
                                if r == c:
                                    for var in seTup:
                                        bits.append(var)
                                    break
                            for var in seTup:
                                bits.append(var)
                        elif (bit_pattern == 'eighth'):
                            eiTup = self.eighth(r, c)
                            if swap:
                                eiTup = list(eiTup)
                                eiTup.reverse()
                            if diagonal:
                                if r == c:
                                    for var in eiTup:
                                        bits.append(var)
                                    break
                            for var in eiTup:
                                bits.append(var)
                        count += 1

            self.bits = "".join(bits)


    def first(self, r, c):
        firstTup = (str(self.img[r,c,0] & 1), str(self.img[r,c,1] & 1), str(self.img[r,c,2] & 1))
        return firstTup

    def second(self, r, c):
        secondTup = (str((self.img[r,c,0] & 2) >> 1), str((self.img[r,c,1] & 2) >> 1), str((self.img[r,c,2] & 2) >> 1))
        return secondTup

    def third(self, r, c):
        thirdTup = (str((self.img[r,c,0] & 4) >> 2), str((self.img[r,c,1] & 4) >> 2), str((self.img[r,c,2] & 4) >> 2))
        return thirdTup

    def fourth(self,  r, c):
        fourthTup = (str((self.img[r,c,0] & 8) >> 3), str((self.img[r,c,1] & 8) >> 3), str((self.img[r,c,2] & 8) >> 3))
        return fourthTup

    def fifth(self, r, c):
        fifthTup = (str((self.img[r,c,0] & 16) >> 4), str((self.img[r,c,1] & 16) >> 4), str((self.img[r,c,2] & 16) >> 4))
        return fifthTup

    def sixth(self, r, c):
        sixthTup = (str((self.img[r,c,0] & 32) >> 5), str((self.img[r,c,1] & 32) >> 5), str((self.img[r,c,2] & 32) >> 5))
        return sixthTup

    def seventh(self, r, c):
        seventhTup = (str((self.img[r,c,0] & 64) >> 6), str((self.img[r,c,1] & 64) >> 6), str((self.img[r,c,2] & 64) >> 6))
        return seventhTup

    def eighth(self, r, c):
        eighthTup = (str((self.img[r,c,0] & 128) >> 7), str((self.img[r,c,1] & 128) >> 7), str((self.img[r,c,2] & 128) >> 7))
        return eighthTup

    def get_bits(self):
        return self.bits

    def width(self):
        return self.width

    def height(self):
        return self.height

    def set_bits(self, bits):
        self.bits = bits

    def save_bits(self,bit_pattern='first', rotation=0, combine=False, channel='all', reversed=False, swap=False, diagonal=False):
        with open (Path('./found_bits/' + os.path.basename(self.path) +  '/' + bit_pattern + 'bits' + 'rotated'+str(rotation)+ 'reversed'+str(reversed)+'swap'+str(swap)+'combined'+str(combine)+'channel'+str(channel)+'diagonal'+str(diagonal)'.txt'), "w+") as f:
            f.write(self.bits)

    def rotate(self, degrees):
        print("Rotating", degrees, 'degrees')
        img = Image.fromarray(self.img)
        img = img.rotate(degrees)
        self.img = np.array(img)
        return self.img

    def get_int(self, bits=None, start=0, stop=8):
        if bits is None:
            bits = self.bits
        return util.ba2int(bitarray.bitarray(bits[start:stop]))

    def get_all_ints(self):

        # Dictionary int : location
        self.all_ints = {}

        counter = 0
        while counter + 32 < self.bitLength:
            try:
                number = util.ba2int(bitarray.bitarray(self.bits[counter:counter+32]))
                self.all_ints.update({counter+32 : number})
            except:
                pass
            counter += 32

        return self.all_ints

class HiddenImage(ImageBits):
    '''
    Class used to detect and translate nested hidden images
    '''

    def __init__(self, path='./samples/hide_image.png', dimensions=(60, 80), bits=None, bit_pattern=None, combine=None, rotation=0, channel=None, reversed=False, swap=False, diagonal=False):
        super().__init__(path, bits=bits, bit_pattern=bit_pattern, combine=combine, rotation=rotation, channel=channel, reversed=reversed, swap=swap)
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
        try:
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

            return hidden_img

        except:
            return None

    def rotate(self, degrees):
        if self.hidden_img is None:
            self.find()
        img = Image.fromarray(self.hidden_img)
        img = img.rotate(degrees)
        self.hidden_img = np.array(img)
        self.save()
        return self.hidden_img

    def stats(self):
        if self.hidden_img is None:
            self.find()
        imgTwo = self.hidden_img
        binary = self.bits[start:]
        for r in range(self.height):
            for c in range(self.width):
                binaryCheck = first(r, c, bits)
                if binaryCheck[0] == 1:
                    imgTwo[r, c, 0] = 255
                elif binaryCheck[0] == 0:
                    imgTwo[r, c, 0] = 0
                if binaryCheck[1] == 1:
                    imgTwo[r, c, 1] = 255
                elif binaryCheck[1] == 0:
                    imgTwo[r, c, 1] = 0
                if binaryCheck[2] == 1:
                    imgTwo[r, c, 2] = 255
                elif binaryCheck[2] == 0:
                    imgTwo[r, c, 2] = 0
        img = self.hidden_img
        self.hidden_img = imgTwo
        self.save()
        self.hidden_img = img
        return True


    def save(self):
        if self.hidden_img is None:
            self.find()
        try:
            imageio.imwrite(Path('./found_images/'+ os.path.basename(self.path) + '/' + datetime.now().strftime("%m:%d:%Y:%H:%M:%S") +'.jpg'), self.hidden_img)
        except:
            print("Error. Saving image was not possible.")
            return False
        return True


class HiddenText(ImageBits):
    def __init__(self, path='./samples/hide_text.png', dimensions=(32, 4580), bits=None, bit_pattern=None, combine=None, rotation=0, channel=None, reversed=False, swap=False, diagonal=False):
        super().__init__(path, bits=bits, bit_pattern=bit_pattern, combine=combine, rotation=rotation, channel=channel, reversed=reversed, swap=swap)
        self.dimensions = dimensions
        self.hidden_text = None
        self.header()

    def __str__(self):
        if self.hidden_text is None:
            return self.find()
        return self.hidden_text

    def header(self, start=0):
        '''
        Converts <binary> to int
        '''
        try:
            self.dimensions=(32, util.ba2int(bitarray.bitarray(self.bits[start:start+32])))
        except:
            'Error converting to Int'
        return self.dimensions[1]

    def find(self, start=None, stop=None):
        '''
        Finds hidden text in its image between <start> and <stop>
        '''
        if start is None: start = self.dimensions[0]
        if stop is None: stop = self.dimensions[1]

        text = None

        counter = start

        text = []

        while counter + 8 < stop and counter+8 < len(self.bits):
            try:
                char = bitarray.bitarray(self.bits[counter:counter+8]).tobytes().decode('ascii')
                text.append(char)
            except:
                print('Error decoding text')
                break
            counter += 8

        text = "".join(text)
        self.hidden_text = text

        return text

    def save(self):
        if self.hidden_text is None:
            self.find()
        try:
            with open (Path('./found_text/'+ os.path.basename(self.path) + '/' + datetime.now().strftime("%m:%d:%Y:%H:%M:%S") +'.txt'), "w+") as f:
                f.write(self.hidden_text)
        except:
            print("Error. Saving text was not possible.")
            return False
        return True

if __name__ == "__main__":
    # Usage
    hi = HiddenImage()
    print(hi)
    hi.rotate(270)

    ht = HiddenText()
    print(ht)
