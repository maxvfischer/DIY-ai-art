import time
import multiprocessing
from kiosk.kiosk import Kiosk
from kiosk.utils import read_yaml
from kiosk.artbutton import ArtButton
from watchdog.observers import Observer
from kiosk.art_event_handler import ArtEventHandler
from kiosk.pir_sensor_screensaver import PIRSensorScreensaver


def start_artbutton(GPIO_mode: str,
                    GPIO_pinout: int,
                    active_artwork_file_path: str,
                    image_directory: str,
                    loop_sleep_sec: float) -> None:
    """
    Starts the art button listener.

    Parameters
    ----------
    GPIO_mode : str
        GPIO mode used to set up the Nvidia Jetson board. Accepted values: {'BOARD', 'BCM'}

    GPIO_pinout : int
        GPIO pin number to which the button is connected.

    active_artwork_file_path : str
        Path to the active artwork file. This is the image that will be displayed in the Kiosk.

    image_directory : str
        Path to the image directory from where the images will be randomly sampled.

    loop_sleep_sec : float
        Seconds to sleep after registered button click. Risk of multiple unexpected simultaneous clicks
        if set to low.

    Returns
    -------
    None
    """
    button = ArtButton(
        GPIO_mode=GPIO_mode,
        GPIO_pinout=GPIO_pinout,
        active_artwork_file_path=active_artwork_file_path,
        image_directory=image_directory,
        loop_sleep_sec=loop_sleep_sec
    )
    button.start()
    

def start_kiosk(active_artwork_file_path: str,
                frame_path: str,
                frame_inner_size: tuple) -> None:
    """
    Starts art kiosk.

    Parameters
    ----------
    active_artwork_file_path : str
        Path to active artwork to be displayed. If the active artwork image is updated, the new image will be rendered.

    frame_path : str
        Path to frame image.

    frame_inner_size : tuple
        Inner size of frame. Used to resize artwork to fit frame.

    Returns
    -------
    None
    """
    kiosk = Kiosk(
        active_artwork_path=active_artwork_file_path, 
        frame_path=frame_path,
        frame_inner_size=frame_inner_size)
    kiosk.start()


def start_pir(GPIO_mode: str,
              GPIO_pinout: int,
              loop_sleep_sec: float,
              screensaver_after_sec: float) -> None:
    """
    Starts passive infrared sensor listener.

    Parameters
    ----------
    GPIO_mode : str
        GPIO mode used to set up the Nvidia Jetson board. Accepted values: {'BOARD', 'BCM'}

    GPIO_pinout : int
        GPIO pin number to which the PIR sensor is connected.

    loop_sleep_sec : float
        Seconds to sleep when reading PIR sensor and checking screensaver.

    screensaver_after_sec : float
        Seconds before the screensaver will be activated.

    Returns
    -------
    None
    """
    pir = PIRSensorScreensaver(
        GPIO_mode=GPIO_mode,
        GPIO_pinout=GPIO_pinout,
        loop_sleep_sec=loop_sleep_sec,
        screensaver_after_sec=screensaver_after_sec
    )
    pir.start()


def start_art_generator(image_directory: str,
                        lower_limit_num_images: int) -> None:
    """
    Starts event handler that listens to deleted images in the image_directory. If an image is deleted from the
    image_directory (i.e. moved to replace the active artwork) and the number of images in image_directory falls
    below lower_limit_num_images, a process is spawned to generate new images.

    NOTE: You need to update the class ArtEventHandler and pass the needed arguments to generate new images!

    Parameters
    ----------
    image_directory : str
        Path to the image directory to where the newly generated images should be saved.

    lower_limit_num_images : int
        Lower threshold triggering new images to be generated.

    Returns
    -------
    None
    """
    handler = ArtEventHandler(
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
        target=start_artbutton,
        args=(
            config['artbutton']['GPIO_mode'],
            config['artbutton']['GPIO_pinout'],
            config['active_artwork_file_path'],
            config['image_directory'],
            config['artbutton']['loop_sleep_sec']
        )
    )

    p_kiosk = multiprocessing.Process(
        target=start_kiosk,
        args=(
            config['active_artwork_file_path'],
            config['kiosk']['path'],
            (config['kiosk']['inner_width'], config['kiosk']['inner_height'])
        )
    )

    p_pir = multiprocessing.Process(
        target=start_pir,
        args=(
            config['pirsensor']['GPIO_mode'],
            config['pirsensor']['GPIO_pinout'],
            config['pirsensor']['loop_sleep_sec'],
            config['pirsensor']['screensaver_after_sec'],
        )
    )

    p_art = multiprocessing.Process(
        target=start_art_generator,
        args=(
            config['image_directory'],
            config['lower_limit_num_images']
        )
    )

    p_button.start()
    p_kiosk.start()
    p_pir.start()
    p_art.start()

    p_button.join()
    p_kiosk.join()
    p_pir.join()
    p_art.join()
