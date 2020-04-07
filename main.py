import os
from pathlib import Path
from detect import HiddenImage, HiddenText
import multiprocessing
import enchant


def make_found_dirs():
    'Make found_images and found_text directories'
    for _, dirnames, filenames in os.walk('./images'):
        for file in filenames:
            # os.mkdir('./found_text/'+file)
            # os.mkdir('./found_images/'+file)
            # os.mkidr('./found_bits/'+file)
            os.mkdir('./all_ints/'+file)

def extract_bits():
    'Extract all bits of each image'
    base_path = Path('./images')

    for _, dirnames, filenames in os.walk(base_path):
        for type in ['first']:
            print('Extracting ' + type + ' bits')

            for image in filenames:
                for rotation in [0]:
                    print('For ' + image)
                    # Get text from HiddenText
                    text = HiddenText(base_path / image, bit_pattern=type, combine='false', rotation=rotation)
                    text.save_bits(type)

def analyze_all():
    base = Path('./found_bits')
    d = enchant.Dict("en_US")
    for _, dirnames, filenames in os.walk(base):
        for directory in dirnames:
            for _, dirnames, filenames in os.walk(base / directory):
                for file in filenames:
                    with open (base / directory / file) as f:

                        original_path = Path('./images/' + directory)
                        bits = f.read()
                        print("Analyzing", directory, file)

                        # Get text
                        text = HiddenText(original_path, bits=bits, bit_pattern='first', combine=False)
                        ints = text.get_all_ints()
                        # Use all the headers as starting points for text
                        for (key, value) in ints.items():
                            print("Examining potential text at index", value)
                            text_message = text.find(start=key, stop=key+(value*8))

                            if text_message is not None:
                                # If we have a string
                                english = False
                                for word in text_message.split():
                                    # Check each word if it's english
                                    try:
                                        is_english = d.check(word)
                                    except:
                                        continue

                                    if is_english and len(word) > 4:
                                        # If it is english, save the message
                                        text.save()
                                        break


                        # Get hidden_img from HiddenImage

                        # img = HiddenImage(original_path, bits=bits, bit_pattern='first', combine=False)
                        # img_header = img.header()
                        # img_img = img.find()
                        # if img_img is not None and 0 not in img_header:
                        #     print(img_img)
                        #     img.save()
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
                text = HiddenText(original_path, bits=bits, bit_pattern='first', combine=False)
                text_header = text.header()

                text_message = text.find(start=0, stop=len(text.get_bits()))
                if text_message is not None:
                    print(text_message)
                    if len(text_message.strip()) > 5:
                        text.save()

                print("\n")

                # Get hidden_img from HiddenImage

                # img = HiddenImage(original_path, bits=bits, bit_pattern='first', combine=False)
                # img_header = img.header(first=1000, second=1000+32)
                # print(img_header)
                #
                # if img_header is not None:
                #     img_img = img.find(start=1512+64, first=1512, second=1512+32)

def get_all_headers():
    base = Path('./found_bits')
    for _, dirnames, filenames in os.walk(base):
        for directory in dirnames:
            for _, dirnames, filenames in os.walk(base / directory):
                for file in filenames:
                    with open (base / directory / file) as f:
                        if 'first' in file:
                            original_path = Path('./images/' + directory)
                            bits = f.read()
                            print("Analyzing " + directory)
                            # Get text
                            text = HiddenText(original_path, bits=bits, bit_pattern='first', combine=False)

                            ints = text.get_all_ints()
                            with open (Path('./all_ints/' + directory +  '/' + 'ints.txt'), "w+") as f:
                                f.write(str(ints))


if __name__ == '__main__':
    # get_all_headers()
    # extract_bits()
    analyze_all()
    # analyze('PuppyLeash.png')
