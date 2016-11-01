# from PIL import Image
# im = Image.open('dataBase/att_faces/s1/1.pgm')
# im.show()
# im.save('out.jpg')

import numpy as np
from PIL import Image
import cv2
import random
from pylab import array, uint8 
from PIL import Image, ImageChops

def normalize(arr):
    """
    Linear normalization
    http://en.wikipedia.org/wiki/Normalization_%28image_processing%29
    """
    arr = arr.astype('float')
    # Do not touch the alpha channel
    for i in range(3):
        minval = arr[...,i].min()
        maxval = arr[...,i].max()
        if minval != maxval:
            arr[...,i] -= minval
            arr[...,i] *= (1.0/(maxval-minval))
    return arr

def contrastBrightess(image):
    contrast = random.uniform(0.5, 2)
    brightness = random.uniform(-20, 50)
    # contrast = 2
    # brightness = 50

    maxIntensity = 255.0 # depends on dtype of image data
    phi = 1
    theta = 1
    image = ((maxIntensity/phi)*(image/(maxIntensity/theta))**contrast) + brightness
    image = np.asarray(image)
    top_index = np.where(image > 255)
    bottom_index = np.where(image < 0)
    image[top_index] = 255
    image[bottom_index] = 0
    image = array(image,dtype=uint8)
    return image


def resize(image):
    (h, w) = image.shape
    ratio = random.uniform(0.5, 1)
    size = (int(w*ratio), int(h*ratio))
    image = Image.fromarray(np.uint8(image))
    image.thumbnail(size, Image.ANTIALIAS)
    image_size = image.size
    thumb = image.crop( (0, 0, w, h) )

    offset_x = max( (w - image_size[0]) / 2, 0 )
    offset_y = max( (h - image_size[1]) / 2, 0 )

    thumb = ImageChops.offset(thumb, offset_x, offset_y)
    image = np.asarray(thumb)
    return image

def generateMoreImg(num, img):
    # imgs = None
    imgs = []
    for i in range(num):
        img1 = contrastBrightess(img)
        img2 = resize(img)
        print img1.shape
        print img2.shape

        imgs.append(img1.ravel())
        imgs.append(img2.ravel())
    return imgs

def demo_normalize():
    # img = Image.open("noSmile.jpg").convert('RGBA')   
    # arr = np.array(img)
    # new_img = Image.fromarray(normalize(arr).astype('uint8'),'RGBA')
    # new_img.save('normalized.png')
    pass

def rotate_image(image):
    w, h = image.shape
    degree = random.uniform(-45, 45)

    M = cv2.getRotationMatrix2D((w/2, h/2),degree,1)
    image = cv2.warpAffine(image,M,(w, h))
    return image

def demo_test():
    img = cv2.imread("noSmile.jpg",0)    
    while True:
        # newImg = contrast_brightess_image(img)
        # newImg = resize(img)
        newImg = rotate_image(img)


        cv2.imshow('Video', newImg)
        cv2.waitKey(100)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # imgs2 = []
    # imgs = generateMoreImg(5, img)
    # print len(imgs)
    # print imgs[0].shape
    # imgs2.extend(imgs)
    # print len(imgs2)
    # print imgs2[0].shape


# demo_normalize()
demo_test()
