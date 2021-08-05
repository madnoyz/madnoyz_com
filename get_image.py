from PIL import Image
import os
import glob

def get_image(directory):
    address =  str(directory) + '/*.png'
    file_list = [os.path.basename(filename.split('\\')[-1]) for filename in glob.glob(address)]
        #im=Image.open(filename)
    return file_list