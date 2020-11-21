import os
import sys
import time
import random
import subprocess
import Jetson.GPIO as GPIO

GPIO_modes = {
    'BOARD': GPIO.BOARD,
    'BCM': GPIO.BCM
}

class Button():
    def __init__(self,
                 GPIO_mode: str,
                 GPIO_button: int,
                 active_artwork_file_path: str,
                 image_directory: str) -> None:
        try:
            mode = GPIO_modes[GPIO_mode]
            GPIO.setmode(mode)
            GPIO.setup(GPIO_button, GPIO.IN)
            self.GPIO_button = GPIO_button
        except Exception as e:
            print(e.message)
            sys.exit(1)

        if ('.jpg' in active_artwork_file_path) and (os.path.isfile(active_artwork_file_path)):
            self.active_artwork_file_path = active_artwork_file_path
        else:
            raise ValueError('Active arwork file is not a .jpg or does not exist.')
        if os.path.isdir(image_directory):
            self.image_directory = image_directory

    def _get_random_image_path(self):
        image_names = [image_name for image_name in os.listdir(self.image_directory) if '.jpg' in image_name]
        image_name = random.choice(image_names)

        image_path = os.path.join(self.image_directory, image_name)
        return image_path


    def _change_active_artwork(self):
        image_path = self._get_random_image_path()
        os.rename(
            src=image_path,
            dst=self.active_artwork_file_path
        )

    def start(self):
        while True:
            input_state = GPIO.input(self.GPIO_button)
            if input_state == False:
                self._change_active_artwork()
                time.sleep(1)


if __name__ == '__main__':
    button = Button(
        GPIO_mode='BOARD',
        GPIO_button=15,
        active_artwork_file_path='active_artwork.jpg',
        image_directory='images'
    )
    button.start()
