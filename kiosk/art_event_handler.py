import os
import multiprocessing
from watchdog.events import FileSystemEventHandler, FileModifiedEvent


class ArtEventHandler(FileSystemEventHandler):
    """
    Event handler generating new images.

    NOTE: Update this class with your code to generate new images!

    Parameters
    ----------
    image_directory : str
        Path to the image directory to where the newly generated images should be saved.

    lower_limit_num_images : int
        Lower threshold triggering new images to be generated.

    """
    def __init__(self,
                 image_directory: str,
                 lower_limit_num_images: int):
        self.image_directory = image_directory
        self.lower_limit_num_images = lower_limit_num_images
        self.generating_images = multiprocessing.Value('b', False)

    def generate_images(self,
                        generating_images: multiprocessing.Value) -> None:
        """
        Generates images to be displayed on the art kiosk.

        This function is executed in its own process when the number of images in the self.image_directory drops
        below the threshold self.lower_limit_num_images.

        NOTE: Add your generative code in this function, replacing the comments below!

        Parameters
        ----------
        generating_images : multiprocessing.Value
            Multiprocessing value variable to keep track if there are images currently being generated.

        Returns
        -------
        None
        """
        generating_images.value = True

        # GENERATE YOUR IMAGES HERE
        # For example:
        # config = tf.ConfigProto(allow_soft_placement=True)
        # with tf.Session(config=config) as sess:
        #     gan = StyleGAN(
        #         sess=sess,
        #         batch_size=self.batch_size,
        #         img_size=self.img_size,
        #         checkpoint_directory=self.checkpoint_directory,
        #         image_directory=self.image_directory)
        #
        #     gan.generate_images(
        #         num_images=self.test_num
        #     )

        generating_images.value = False

    def on_deleted(self,
                   event) -> None:
        """
        Function triggered when an image is deleted from the image directory. If number of images in
        self.image_directory falls below the threshold self.lower_limit_num_images, it spawns a new process generating
        new images.

        Parameters
        ----------
        event : -
            -

        Returns
        -------
        None
        """
        image_names = [image_name for image_name in os.listdir(self.image_directory) if '.jpg' in image_name]
        num_images = len(image_names)
        if (num_images < self.lower_limit_num_images) and (self.generating_images.value == False):
            p_generate = multiprocessing.Process(
                target=self.generate_images,
                args=(self.generating_images,)
            )
            p_generate.start()
