#!/home/pi/spotmicroai/venv/bin/python3 -u

import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from pick import pick
import time

from spotmicro.utilities.log import Logger
from spotmicro.utilities.config import Config

log = Logger().setup_logger('CALIBRATE SERVOS')

log.info('Calibrate rest position...')

pca9685_1_address = int(Config().get(Config.MOTION_CONTROLLER_BOARDS_PCA9685_1_ADDRESS), 0)
pca9685_1_reference_clock_speed = int(Config().get(Config.MOTION_CONTROLLER_BOARDS_PCA9685_1_REFERENCE_CLOCK_SPEED))
pca9685_1_frequency = int(Config().get(Config.MOTION_CONTROLLER_BOARDS_PCA9685_1_FREQUENCY))

boards = 1

try:
    pca9685_2_address = int(
        Config().get(Config.MOTION_CONTROLLER_BOARDS_PCA9685_2_ADDRESS), 0)

    if pca9685_2_address:
        pca9685_2_reference_clock_speed = int(Config().get(Config.MOTION_CONTROLLER_BOARDS_PCA9685_2_REFERENCE_CLOCK_SPEED))
        pca9685_2_frequency = int(Config().get(Config.MOTION_CONTROLLER_BOARDS_PCA9685_2_FREQUENCY))
        boards = 2

except:
    log.error("Second PCA not found")

log.info('Use the command "i2cdetect -y 1" to list your i2c devices connected and')
log.info('write your pca9685 i2c address(es) and settings in your configuration file ~/spotmicroai.json')
log.info('There is configuration present for ' + str(boards) + ' boards')

pca = None

i2c = busio.I2C(SCL, SDA)

options = {0: 'rear_shoulder_left',
           1: 'rear_leg_left',
           2: 'rear_feet_left',
           3: 'rear_shoulder_right',
           4: 'rear_leg_right',
           5: 'rear_feet_right',
           6: 'front_shoulder_left',
           7: 'front_leg_left',
           8: 'front_feet_left',
           9: 'front_shoulder_right',
           10: 'front_leg_right',
           11: 'front_feet_right'}

title = 'Please choose the servo to calibrate its rest position: '
screen_options = list(options.values())

selected_option, selected_index = pick(screen_options, title)

PCA9685_ADDRESS, PCA9685_REFERENCE_CLOCK_SPEED, PCA9685_FREQUENCY, CHANNEL, MIN_PULSE, MAX_PULSE, REST_ANGLE = Config.get_by_section_name(selected_option)

while True:

    try:
        angle = input("Write your angle and press Enter: ")

        pca = PCA9685(i2c, address=int(PCA9685_ADDRESS, 0), reference_clock_speed=PCA9685_REFERENCE_CLOCK_SPEED)
        pca.frequency = PCA9685_FREQUENCY

        active_servo = servo.Servo(pca.channels[CHANNEL])
        active_servo.set_pulse_width_range(min_pulse=MIN_PULSE, max_pulse=MAX_PULSE)

        if angle == '':
            angle = 90

        active_servo.angle = int(angle)
        time.sleep(0.1)
    finally:
        pca.deinit()
