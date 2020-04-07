import os
from pathlib import Path
from detect import HiddenImage, HiddenText
import multiprocessing


def make_found_dirs():
    'Make found_images and found_text directories'
    for _, dirnames, filenames in os.walk('./images'):
        for file in filenames:
            # os.makedirs('./found_text/'+file)
            # os.makedirs('./found_images/'+file)
            os.makedirs('./found_bits/'+file)

def extract_bits():
    'Extract all bits of each image'
    base_path = Path('./images')

    for _, dirnames, filenames in os.walk(base_path):
        for image in filenames:
            # From Left to Right and Right to Left
            for reversed in [True, False]:
                # No rotation
                for rotation in [0]:
                    # Get a bit for each channel
                    for channel in range(3):
                        print('For', image, 'extracting', 'reversed', reversed, 'rotation', rotation, 'channel', channel)
                        # Get text from HiddenText
                        text = HiddenText(base_path / image, bit_pattern='channel', combine=False, rotation=rotation, channel=channel, reversed=reversed)
                        text.save_bits(bit_pattern='channel', rotation=rotation, combine=False, channel=channel, reversed=reversed)
                    # RGB or BGR?
                    for swap in [True, False]:
                        # Combine all bits up including the fourth one
                        for type in ['fourth']:
                            print('For', image, 'extracting', 'reversed', reversed, 'rotation', rotation, 'swap', swap, 'type', type)
                            # Get text from HiddenText (combining all 4th bits)
                            text = HiddenText(base_path / image, bit_pattern=type, combine='true', rotation=rotation, channel=None, reversed=reversed, swap=swap)
                            text.save_bits(bit_pattern=type, rotation=rotation, combine='true', reversed=reversed, swap=swap)

                        # Extract only the first bit. Then extract only the second bit.
                        for type in ['first', 'second']:
                            print('For', image, 'extracting', 'reversed', reversed, 'rotation', rotation, 'swap', swap, 'type', type)
                            # Get text from HiddenText (combining all 4th bits)
                            text = HiddenText(base_path / image, bit_pattern=type, combine=False, rotation=rotation, channel=None, reversed=reversed, swap=swap)
                            text.save_bits(bit_pattern=type, rotation=rotation, combine=False, reversed=reversed, swap=swap)


def analyze_all():
    base = Path('./found_bits')
    for _, dirnames, filenames in os.walk(base):
        for directory in dirnames:
            for _, dirnames, filenames in os.walk(base / directory):
                for file in filenames:
                    with open (base / directory / file) as f:
                        original_path = Path('./images/' + directory)
                        bits = f.read()
                        for location in [0, 1, 2, 1000, 1001, 1002]:
                            print("Analyzing", directory, file, "at location", location)
                            # Get text
                            text = HiddenText(original_path, bits=bits, bit_pattern='first', combine=False)
                            text_header = text.header(location)
                            if text_header is not None and text_header < 10000:
                                text_message = text.find(start=location+32, stop=len(bits))

                                if text_message is not None and len(text_message.strip()) > 5:
                                    print(text_message)
                                    text.save()

                            # Get hidden_img from HiddenImage
                            img = HiddenImage(original_path, bits=bits, bit_pattern='first', combine=False)
                            img_header = img.header(location, location+32)

                            if img_header is not None and img_header[0] < 10000 and 0 not in img_header:
                                img_img = img.find(start=location+64)
                                if img_img is not None:
                                    print(img_img)
                                    img.save()

                            print('\n')

def analyze(name):
    '''
    For a specific image, look at all its different bit compositions to find
    messages.
    '''
    for _, dirnames, filenames in os.walk(Path('./found_bits/' + name)):
        for file in filenames:
            with open (Path('./found_bits/' + name + '/' + file)) as f:

                original_path = Path('./images/' + name)
                bits = f.read()

                print("Analyzing", name, file)

                # Get text

                # text = HiddenText(original_path, bits=bits, bit_pattern='first', combine=False)
                # text_header = text.header()
                # print(text_header)

                # text_message = text.find(stop=367)
                # if text_message is not None:
                #     print(text_message)
                #     text.save()

                print("\n")

                # Get hidden_img from HiddenImage

                img = HiddenImage(original_path, bits=bits, bit_pattern='first', combine=False)
                img_header = img.header(first=0, second=32)
                print(img_header)

                if img_header is not None:
                    img_img = img.find(start=64, w=img_header[0], h=img_header[1])
                    img.save()

if __name__ == '__main__':
    # make_found_dirs()
    # extract_bits()
    analyze_all()
    # analyze('WinkyFace.png')
