import os
import multiprocessing
import tensorflow as tf
from ml.StyleGAN import StyleGAN
from watchdog.events import FileSystemEventHandler, FileModifiedEvent


class ArtEventHandler(FileSystemEventHandler):
    def __init__(self,
                 batch_size: int,
                 img_size: int,
                 test_num: int,
                 checkpoint_directory: str,
                 image_directory: str,
                 lower_limit_num_images: int):
        self.batch_size = batch_size
        self.img_size = img_size
        self.test_num = test_num
        self.checkpoint_directory = checkpoint_directory
        self.image_directory = image_directory
        self.lower_limit_num_images = lower_limit_num_images
        self.generating_images = multiprocessing.Value('b', False)

    def generate_images(self,
                        generating_images):
        generating_images.value = True

        config = tf.ConfigProto(allow_soft_placement=True)
        with tf.Session(config=config) as sess:
            gan = StyleGAN(
                sess=sess,
                batch_size=self.batch_size,
                img_size=self.img_size,
                checkpoint_directory=self.checkpoint_directory,
                image_directory=self.image_directory)

            gan.generate_images(
                num_images=self.test_num
            )

        generating_images.value = False

    def on_deleted(self,
                   event):
        image_names = [image_name for image_name in os.listdir(self.image_directory) if '.jpg' in image_name]
        num_images = len(image_names)
        if (num_images < self.lower_limit_num_images) and (self.generating_images.value == False):
            p_generate = multiprocessing.Process(
                target=self.generate_images,
                args=(self.generating_images,)
            )
            p_generate.start()
