import queue
import random
import math
import time
import copy
from random import randint
from PIL import Image

if __name__ == '__main__' :

    img = Image.open("image_0.jpg")
    width, height = img.size
    left_half = (0, 0, width/2, height)
    right_half = (width/2, 0, width, height)
    testing_img = img.crop(right_half)
    training_img = img.crop(left_half)
    testing_img.save("testing_data.jpg")
    training_img.save("training_data.jpg")