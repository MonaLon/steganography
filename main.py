import os
from pathlib import Path
from detect import HiddenImage, HiddenText

if __name__ == '__main__':

    base_path = Path('./images')

    for _, dirnames, filenames in os.walk(base_path):

            for image in filenames:
                # Get text from HiddenText
                text = HiddenText(base_path / image, bit_pattern='first', combine=False)
                text.save_bits('first')
                # text_header = text.header()
                # text_message = text.find()
                #
                # # Get hidden_img from HiddenImage
                # img = HiddenImage(base_path / image, bits=text.get_bits())
                # img_header = img.header()
                # if img_header is not None:
                #     img_img = img.find()
