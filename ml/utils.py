import numpy as np
import os
from glob import glob
from ml.ops import lerp

import tensorflow as tf
import tensorflow.contrib.slim as slim
import cv2


def check_folder(log_dir):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    return log_dir

def save_images(images, size, image_path):
    # return imsave(inverse_transform(images), size, image_path)
    return imsave(images, size, image_path)


def imsave(images, size, path):
    # return scipy.misc.imsave(path, merge(images, size))

    images = merge(images, size)
    images = post_process_generator_output(images)
    images = cv2.cvtColor(images.astype('uint8'), cv2.COLOR_RGB2BGR)
    images = cv2.resize(images, (1920, 1080))
    cv2.imwrite(path, images)


def merge(images, size):
    h, w = images.shape[1], images.shape[2]
    c = images.shape[3]
    img = np.zeros((h * size[0], w * size[1], c))
    for idx, image in enumerate(images):
        i = idx % size[1]
        j = idx // size[1]
        img[h*j:h*(j+1), w*i:w*(i+1), :] = image

    return img


def post_process_generator_output(generator_output):

    drange_min, drange_max = -1.0, 1.0
    scale = 255.0 / (drange_max - drange_min)

    scaled_image = generator_output * scale + (0.5 - drange_min * scale)
    scaled_image = np.clip(scaled_image, 0, 255)

    return scaled_image


def str2bool(x):
    return x.lower() in ('true')
