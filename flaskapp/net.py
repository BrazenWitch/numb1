import os
# модуль работы с изображениями
from PIL import Image
import numpy as np
import sys
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import random

def red_image(image_):
    image_ = image_.sum(axis=2)/3.0 
    image_new = np.zeros((224,224,3))
    image_new [:,:,0]= image_ 
    return image_new

image = Image.open('static/uvkX7vXQC2I.jpg')

'''height = 224
width = 224
images_resized = np.array(image.resize(height,width))/255.0
images_resized = np.array(images_resized)'''
image1 = np.array(image)

fig_ = plt.figure(figsize=(1,1))
viewer = fig_.add_subplot(1,1,1)

image_ = image1.copy()
viewer.imshow(image1)

plt.show()
