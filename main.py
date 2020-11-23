import time
import multiprocessing
from kiosk.arthur import Arthur
from kiosk.utils import read_yaml
from kiosk.aiartbutton import AiArtButton
from ml.StyleGAN import GANEventHandler
import tensorflow as tf
from watchdog.observers import Observer

def start_aiartbutton(GPIO_mode: str,
                      GPIO_button: int,
                      active_artwork_file_path: str,
                      image_directory: str,
                      button_sleep: float):
    button = AiArtButton(
        GPIO_mode=GPIO_mode,
        GPIO_button=GPIO_button,
        active_artwork_file_path=active_artwork_file_path,
        image_directory=image_directory,
        button_sleep=button_sleep
    )
    button.start()
    

def start_kiosk(active_artwork_file_path: str):
    arthur = Arthur(active_artwork_path=active_artwork_file_path)
    arthur.start()
    arthur.tk.mainloop()


def start_gan(batch_size: int,
              img_size: int,
              test_num: int,
              checkpoint_directory: str,
              image_directory: str,
              lower_limit_num_images: int) -> None:
    handler = GANEventHandler(
        batch_size=batch_size,
        img_size=img_size,
        test_num=test_num,
        checkpoint_directory=checkpoint_directory,
        image_directory=image_directory,
        lower_limit_num_images=lower_limit_num_images
    )
    observer = Observer()
    observer.schedule(handler, path=image_directory, recursive=False)
    observer.start()

    while True:
        time.sleep(1)


if __name__ == '__main__':
    config = read_yaml('config.yaml')
    
    p_button = multiprocessing.Process(
        target=start_aiartbutton,
        args=(
            config['aiartbutton']['GPIO_mode'],
            config['aiartbutton']['GPIO_button'],
            config['active_artwork_file_path'],
            config['aiartbutton']['image_directory'],
            config['aiartbutton']['button_sleep']
        )
    )
    p_kiosk = multiprocessing.Process(
        target=start_kiosk,
        args=(config['active_artwork_file_path'], )
    )

    p_ml = multiprocessing.Process(
        target=start_gan,
        args=(
            config['ml_model']['batch_size'],
            config['ml_model']['img_size'],
            config['ml_model']['test_num'],
            config['ml_model']['checkpoint_directory'],
            config['ml_model']['image_directory'],
            config['ml_model']['lower_limit_num_images']
        )
    )

    p_button.start()
    p_kiosk.start()
    p_ml.start()

    p_button.join()
    p_kiosk.join()
    p_ml.join()