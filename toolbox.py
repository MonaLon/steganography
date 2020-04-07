def make_found_dirs():
    'Make found_images and found_text directories'
    for _, dirnames, filenames in os.walk('./images'):
        for file in filenames:
            # os.mkdir('./found_text/'+file)
            # os.mkdir('./found_images/'+file)
            # os.mkidr('./found_bits/'+file)
            # os.mkdir('./all_ints/'+file)
            os.mkdir('./magnified/'+file)
    return True

def magnify():
    for _, dirnames, filenames in os.walk('./images'):
        for file in filenames:
            img = imageio.imread(Path('./images/' + file))
            height, width, _ = img.shape
            bitLength = height * width

            for r in range(height):
                for c in range(width):
                    



if __name__ == '__main__':
    make_found_dirs()
    magnify()
