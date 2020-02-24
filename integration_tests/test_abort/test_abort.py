#!/home/pi/spotmicro/venv/bin/python3 -u

import RPi.GPIO as GPIO
import time

from spotmicro.utilities.log import Logger
from spotmicro.utilities.config import Config

log = Logger().setup_logger('Test Abort')

log.info('Testing abort mechanism...')

gpio_port = Config().get('abort_controller[0].gpio_port')

log.info('Make sure you have connected your GPIO pin to the 0E port in the PCA9685 boards')
log.info('GPIO information for RaspberryPi can be found here: ')
log.info('     https://www.raspberrypi.org/documentation/usage/gpio/')
log.info('Current configuration value is: ' + str(gpio_port))
input("Press Enter to start the tests...")

try:

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio_port, GPIO.OUT)

    GPIO.output(gpio_port, False)
    time.sleep(2)

    GPIO.output(gpio_port, True)
    time.sleep(2)

    GPIO.output(gpio_port, False)
    time.sleep(2)

finally:
    GPIO.cleanup()
