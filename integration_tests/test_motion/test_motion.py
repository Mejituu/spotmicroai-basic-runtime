#!/home/pi/spotmicroai/venv/bin/python3 -u

# Example based from https://github.com/adafruit/Adafruit_CircuitPython_PCA9685/blob/master/examples/pca9685_servo.py
# Servo library used to simplify: https://github.com/adafruit/Adafruit_CircuitPython_Motor/blob/master/adafruit_motor/servo.py

# reference_clock_speed from: https://github.com/adafruit/Adafruit_CircuitPython_PCA9685/blob/master/examples/pca9685_calibration.py

import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
import time

from spotmicro.utilities.log import Logger
from spotmicro.utilities.config import Config

log = Logger().setup_logger('Test Motion')

log.info('Testing Motion...')

pca9685_1_address = int(
    Config().get('motion_controller[*].boards[*].pca9685_1[*].address | [0] | [0] | [0]'), 0)
pca9685_1_reference_clock_speed = int(Config().get(
    'motion_controller[*].boards[*].pca9685_1[*].reference_clock_speed | [0] | [0] | [0]'))
pca9685_1_frequency = int(
    Config().get('motion_controller[*].boards[*].pca9685_1[*].frequency | [0] | [0] | [0]'))

pca9685_2_address = int(
    Config().get('motion_controller[*].boards[*].pca9685_2[*].address | [0] | [0] | [0]'), 0)
boards = 1

if pca9685_2_address:
    pca9685_2_reference_clock_speed = int(Config().get(
        'motion_controller[*].boards[*].pca9685_2[*].reference_clock_speed | [0] | [0] | [0]'))
    pca9685_2_frequency = int(Config().get(
        'motion_controller[*].boards[*].pca9685_2[*].frequency | [0] | [0] | [0]'))
    boards = 2

log.info('Use the command "i2cdetect -y 1" to list your i2c devices connected and')
log.info('write your pca9685 i2c address(es) and settings in your configuration file ~/spotmicroai.json')
log.info('There is configuration present for ' + str(boards) + ' boards')

input("Press Enter to start the tests...")

try:

    i2c = busio.I2C(SCL, SDA)

    pca = PCA9685(i2c, address=pca9685_1_address,
                  reference_clock_speed=pca9685_1_reference_clock_speed)
    pca.frequency = 50

    servo_0 = servo.Servo(pca.channels[0])
    servo_0.set_pulse_width_range(min_pulse=500, max_pulse=2500)

    # Move by angle
    servo_0.angle = 90
    time.sleep(2)

    servo_0.angle = 100
    time.sleep(2)

    servo_0.angle = 90
    time.sleep(2)

    servo_0.angle = 80
    time.sleep(2)

    if boards == 2:
        pca = PCA9685(i2c, address=pca9685_2_address,
                      reference_clock_speed=pca9685_2_reference_clock_speed)
        pca.frequency = 50

        servo_0 = servo.Servo(pca.channels[0])
        servo_0.set_pulse_width_range(min_pulse=500, max_pulse=2500)

        # Move by angle
        servo_0.angle = 90
        time.sleep(2)

        servo_0.angle = 100
        time.sleep(2)

        servo_0.angle = 90
        time.sleep(2)

        servo_0.angle = 80
        time.sleep(2)


finally:
    pca.deinit()
