#!/home/pi/spotmicro/venv/bin/python3 -u

import RPi.GPIO as GPIO
import time

from spotmicro.utilities.log import Logger
from spotmicro.utilities.config import Config

log = Logger().setup_logger('Testing abort mechanism')

try:

    gpio_port = Config().get('abort_controller[0].gpio_port')

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio_port, GPIO.OUT)

    time.sleep(1)
    GPIO.output(gpio_port, False)
    time.sleep(2)

finally:
    GPIO.cleanup()
