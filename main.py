import os
from pathlib import Path
from detect import HiddenImage, HiddenText

if __name__ == '__main__':

    base_path = Path('./images')

    for _, dirnames, filenames in os.walk(base_path):
            images = filenames

    first = HiddenText(base_path / images[0])
    first_header = first.header()
    first_message = first.find(stop=first_header)
