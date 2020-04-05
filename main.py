import os
from pathlib import Path
from detect import HiddenImage, HiddenText
import multiprocessing


def make_found_dirs():
    'Make found_images and found_text directories'
    for _, dirnames, filenames in os.walk('./images'):
        for file in filenames:
            os.mkdir('./found_text/'+file)
            os.mkdir('./found_images/'+file)
            os.mkidr('./found_bits/'+file)

def extract_bits():
    'Extract all bits of each image'
    base_path = Path('./images')

    for _, dirnames, filenames in os.walk(base_path):
        for type in ['first']:
            print('Extracting ' + type + ' bits')

            for image in filenames:
                for rotation in [90, 270]:
                    print('For ' + image)
                    # Get text from HiddenText
                    text = HiddenText(base_path / image, bit_pattern=type, combine=False, rotation=rotation)
                    text.save_bits(type)

def analyze_all():
    base = Path('./found_bits')
    for _, dirnames, filenames in os.walk(base):
        for directory in dirnames:
            for _, dirnames, filenames in os.walk(base / directory):
                for file in filenames:
                    with open (base / directory / file) as f:
                        original_path = Path('./images/' + directory)
                        bits = f.read()
                        print("Analyzing " + directory)
                        # Get text
                        text = HiddenText(original_path, bits=bits, bit_pattern='first', combine=False)
                        text_header = text.header()
                        print(text_header)
                        text_message = text.find(stop=text_header*8)
                        if text_message is not None:
                            print(text_message)
                            text.save()

                        # Get hidden_img from HiddenImage
                        img = HiddenImage(original_path, bits=bits, bit_pattern='first', combine=False)
                        img_header = print(img.header())
                        img_img = img.find()
                        if img_img is not None:
                            img.save()


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
                text = HiddenText(original_path, bits=bits, bit_pattern='first', combine=False)
                text_header = text.header()
                print(text_header)

                text_message = text.find(stop=215)
                # if text_message is not None: text.save()
                print("\n")

                # Get hidden_img from HiddenImage
                img = HiddenImage(original_path, bits=bits, bit_pattern='first', combine=False)
                img_header = print(img.header(32, 64))

                if img_header is not None:
                    img_img = img.find()

if __name__ == '__main__':
    # extract_bits()
    analyze_all()
    # analyze('TheGrassIsGreener.png')
