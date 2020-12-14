import Jetson.GPIO as GPIO
from datetime import datetime
from kiosk.utils import GPIO_MODES


class PIRSensor():
    """
    Listens to PIR sensor and activate screensaver if no movement.

    Parameters
    ----------
    GPIO_mode : str
        GPIO mode used to set up the Nvidia Jetson board. Accepted values: {'BOARD', 'BCM'}

    GPIO_sensor : int
        GPIO pin number to which the PIR sensor is connected.

    loop_sleep_ms : int, default=100
        Seconds to sleep when reading PIR sensor and checking screensaver.

    screen_saver_after_sec : int
        Seconds before the screensaver will be activated.
    """
    def __init__(GPIO_mode: str,
                 GPIO_sensor: int,
                 loop_sleep_ms: int = 100,
                 screen_saver_after_sec: int = 10):
        try:
            mode = GPIO_MODES[GPIO_mode]
            GPIO.setmode(mode)
            GPIO.setup(GPIO_sensor, GPIO.IN)
            self.GPIO_sensor = GPIO_sensor
        except Exception as e:
            print(e.message)
            sys.exit(1)
        self.loop_sleep_ms = loop_sleep_ms
        self.screen_saver_after_sec = screen_saver_after_sec
        self.datetime_last_pir_firing = datetime.now()
        self.screensaver_active = False
    
