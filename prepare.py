#setup

import numpy as np
import math
import os
import glob
import pickle
from PIL import Image

DIM = 3

#from network import generator,discriminator
#from network2 import generator,discriminator


IMAGE_PATH = "./down/*" 
GENERATED_IMAGE_PATH = "./prepared/" 

def data_import(width,height):
    try:
        with open("../" + DRIVE_PATH + 'images%d.pickle'%width, 'rb') as f:
            image = pickle.load(f)
            print("image load from pickle")
    except:
        image = np.empty((0,height,width,DIM), dtype=np.uint8)
        list=sorted(glob.glob(IMAGE_PATH))
        number = 2432
        for i in list:
            number = number + 1
            im_reading = Image.open(i)
            im_reading .thumbnail((width, height),Image.ANTIALIAS)
            print(im_reading.size)
            bg = Image.new("RGBA",[width,height],(255,255,255,255))
            bg.paste(im_reading,(int((width-im_reading.size[0])/2),int((height-im_reading.size[1])/2)))
            im_reading=bg.copy()
            #im_reading.show()
            
            if im_reading.mode=="RGB":
                im_reading = np.array(im_reading)
                
            else: 
                im_reading = im_reading.convert("RGB")
                im_reading = np.array(im_reading)
                print(im_reading.shape)
                cond_p = (im_reading[..., 0] == 0) & (im_reading[..., 1] == 0) & (im_reading[..., 2] == 0)
                im_reading[cond_p] = [255, 255, 255]
                cond_p = (im_reading[..., 0] == 71) & (im_reading[..., 1] == 112) & (im_reading[..., 2] == 76)
                im_reading[cond_p] = [255, 255, 255]
                cond_p = (im_reading[..., 0] == 76) & (im_reading[..., 1] == 105) & (im_reading[..., 2] == 113)
                im_reading[cond_p] = [255, 255, 255]

            print(i)
            
            #im_reading = im_reading.transpose(1,0,2)
            print(im_reading.shape)
            #image = np.append(image, [im_reading], axis=0)
            save_images(im_reading,str(number))

    return image

def save_images(images,file_name):
    if not os.path.exists(GENERATED_IMAGE_PATH):
                    os.mkdir(GENERATED_IMAGE_PATH)
    Image.fromarray(images.astype(np.uint8))\
        .save(GENERATED_IMAGE_PATH+"%s.png" % (file_name))