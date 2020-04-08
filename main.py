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
            # Don't do the ones we already have a message for hehe
            if 'Gadget.png' in image or 'TripleThreat.png' in image or 'PuppyLeash.png' in image or 'Brothers_small.png' in image or 'WideDogIsWide.png' in image or 'PupFriends.png' in image or 'FriendlyPupper.png' in image or 'TheGrassIsGreener.png' in image or 'Brothers.png' in image:
                continue

            # Extract only the first bit. Alpha channel is done automatically.
            for type in ['first']:
                # Just diagonal bits or all bits?
                for diagonal in [True, False]:
                    # Also read in alpha channel
                    for alpha in [True, False]:
                        # From Left to Right and Right to Left
                        for reversed in [True, False]:
                            # RGB or BGR?
                            for swap in [True]:
                                print('For', image, 'extracting', 'swap', swap, 'type', type, 'reversed', reversed, 'alpha', alpha, 'diagonal', diagonal)
                                # Get text from HiddenText (combining all 4th bits)
                                text = HiddenText(base_path / image, bit_pattern=type, combine=False, channel=None,  swap=swap, reversed=reversed, alpha=alpha, diagonal=diagonal)
                                text.save_bits(bit_pattern=type, combine=False, swap=swap, reversed=reversed, alpha=alpha, diagonal=diagonal)


            # Combine all bits up including the fourth one
            for type in ['fourth']:
                for alpha in [False]:
                    print('For', image, 'extracting', 'combined' 'type', type)
                    # Get text from HiddenText (combining all 4th bits)
                    text = HiddenText(base_path / image, bit_pattern=type, combine='true', alpha=alpha)
                    text.save_bits(bit_pattern=type, combine='true', alpha=alpha)

            # Just each channel
            for channel in range(4):
                print('For', image, 'extracting', 'channel', channel)
                # Get text from HiddenText
                try:
                    if channel == 3:
                        text = HiddenText(base_path / image, bit_pattern='channel', combine=False, channel=channel, alpha=True)
                        text.save_bits(bit_pattern='channel', combine=False, channel=channel, alpha=True)
                    else:
                        text = HiddenText(base_path / image, bit_pattern='channel', combine=False, channel=channel)
                        text.save_bits(bit_pattern='channel', combine=False, channel=channel)
                except:
                    print('No alpha channel to extract.')
                    pass


def analyze_all():
    base = Path('./found_bits')
    for _, dirnames, filenames in os.walk(base):
        for directory in dirnames:
            # Don't do the ones we already have a message for hehe
            if 'Gadget.png' in directory or 'TripleThreat.png' in directory or 'PuppyLeash.png' in directory or 'Brothers_small.png' in directory or 'WideDogIsWide.png' in directory or 'PupFriends.png' in directory or 'FriendlyPupper.png' in directory:
                continue
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
                            if text_header is not None:
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
