import os
import sys
import time
import Jetson.GPIO as GPIO
from datetime import datetime
from kiosk.utils import GPIO_MODES


class PIRSensorScreensaver:
    """
    Listens to PIR sensor and activates screensaver if no movement.

    Parameters
    ----------
    GPIO_mode : str
        GPIO mode used to set up the Nvidia Jetson board. Accepted values: {'BOARD', 'BCM'}

    GPIO_pinout : int
        GPIO pin number to which the PIR sensor is connected.

    loop_sleep_sec : float, default=0.1
        Seconds to sleep when reading PIR sensor and checking screensaver.

    screensaver_after_sec : float, default=10.
        Seconds before the screensaver will be activated.
    """
    def __init__(self,
                 GPIO_mode: str,
                 GPIO_pinout: int,
                 loop_sleep_sec: float = 0.1,
                 screensaver_after_sec: float = 10.):
        try:
            mode = GPIO_MODES[GPIO_mode]
            GPIO.setmode(mode)
            GPIO.setup(GPIO_pinout, GPIO.IN)
            self.GPIO_pinout = GPIO_pinout
        except Exception as e:
            print(e.message)
            sys.exit(1)
        self.loop_sleep_sec = loop_sleep_sec
        self.screensaver_after_sec = screensaver_after_sec
        self.datetime_last_pir_firing = datetime.now()
        self.screensaver_active = False

    def _check_change_pir_sensor(self) -> None:
        """Check PIR sensor for movement. If firing, update datetime of last pir firing."""
        sensor_is_firing = GPIO.input(self.GPIO_pinout)
        if sensor_is_firing == True:
           self.datetime_last_pir_firing = datetime.now()

    def _handle_screensaver(self) -> None:
        """Handling if screensaver should be activated/deactivated, depending on PIR sensor."""
        sec_since_pir_firing = (datetime.now() - self.datetime_last_pir_firing).seconds

        # TODO: Fix weird behavior when screensaver is deactivated with keyboard/mouse.
        if (sec_since_pir_firing > self.screensaver_after_sec) and (not self.screensaver_active):
            os.popen('xscreensaver-command -activate')
            self.screensaver_active = True
        elif (sec_since_pir_firing <= self.screensaver_after_sec) and (self.screensaver_active):
            os.popen('xscreensaver-command -deactivate')
            self.screensaver_active = False

    def start(self) -> None:
        """Start PIR Sensor listener"""
        while True:
            self._check_change_pir_sensor()
            self._handle_screensaver()
            time.sleep(self.loop_sleep_sec)