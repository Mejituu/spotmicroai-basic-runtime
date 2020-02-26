import signal
import sys

import queue

import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
import time

from spotmicro.utilities.log import Logger
from spotmicro.utilities.config import Config
import spotmicro.utilities.queues as queues

log = Logger().setup_logger('Motion controller')


class MotionController:
    boards = 1

    is_activated = False

    i2c = None
    pca9685_1 = None
    pca9685_2 = None

    pca9685_1_address = None
    pca9685_1_reference_clock_speed = None
    pca9685_1_frequency = None
    pca9685_2_address = None
    pca9685_2_reference_clock_speed = None
    pca9685_2_frequency = None

    def __init__(self, communication_queues):

        try:

            log.debug('Starting controller...')

            signal.signal(signal.SIGINT, self.exit_gracefully)
            signal.signal(signal.SIGTERM, self.exit_gracefully)

            self.i2c = busio.I2C(SCL, SDA)
            self.load_pca9685_boards_configuration()

            self._abort_queue = communication_queues[queues.ABORT_CONTROLLER]
            self._motion_queue = communication_queues[queues.MOTION_CONTROLLER]
            self._lcd_screen_queue = communication_queues[queues.LCD_SCREEN_CONTROLLER]

            if self.pca9685_2_address:
                self._lcd_screen_queue.put('motion_controller_1 OK')
                self._lcd_screen_queue.put('motion_controller_2 OK')
            else:
                self._lcd_screen_queue.put('motion_controller_1 OK')
                self._lcd_screen_queue.put('motion_controller_2 NOK')

            self._previous_event = {}

        except Exception as e:
            log.error('Motion controller initialization problem', e)
            self._lcd_screen_queue.put('motion_controller_1 NOK')
            self._lcd_screen_queue.put('motion_controller_2 NOK')
            try:
                self.pca9685_1.deinit()
            finally:
                try:
                    if self.boards == 2:
                        self.pca9685_2.deinit()
                finally:
                    sys.exit(1)

    def exit_gracefully(self, signum, frame):
        try:
            self.pca9685_1.deinit()
        finally:
            try:
                if self.boards == 2:
                    self.pca9685_2.deinit()
            finally:
                log.info('Terminated')
                sys.exit(0)

    def do_process_events_from_queues(self):

        while True:

            try:

                # If we don't get an order in 30 seconds we staydown the robot.
                event = self._motion_queue.get(block=True, timeout=30)

                # log.debug(event)

                event_diff = {}
                if self._previous_event:
                    for key in event:
                        if event[key] != self._previous_event[key]:
                            event_diff[key] = event[key]

                if event['start']:
                    if self.is_activated:
                        self.deactivate_pca9685_boards()
                    else:
                        self.activate_pca9685_boards()
                    self.is_activated = not self.is_activated

                if event['a']:
                    print('A')
                    self.rest_position()

                if event['b']:
                    print('B')
                    self.move_forward()

                self._previous_event = event

            except queue.Empty as e:
                # If we don't get an order in 30 seconds we staydown the robot.
                log.info('Inactivity lasted 30 seconds, shutting down the servos, '
                         'press start to reactivate')
                self.deactivate_pca9685_boards()

            except Exception as e:
                log.error('Unknown problem while processing the queue of the motion controller', e)

    def load_pca9685_boards_configuration(self):
        self.pca9685_1_address = int(Config().get(Config.MOTION_CONTROLLER_BOARDS_PCA9685_1_ADDRESS), 0)
        self.pca9685_1_reference_clock_speed = int(
            Config().get(Config.MOTION_CONTROLLER_BOARDS_PCA9685_1_REFERENCE_CLOCK_SPEED))
        self.pca9685_1_frequency = int(Config().get(Config.MOTION_CONTROLLER_BOARDS_PCA9685_1_FREQUENCY))

        self.pca9685_2_address = False
        try:
            self.pca9685_2_address = int(Config().get(Config.MOTION_CONTROLLER_BOARDS_PCA9685_2_ADDRESS), 0)

            if self.pca9685_2_address:
                self.pca9685_2_reference_clock_speed = int(Config().get(
                    Config.MOTION_CONTROLLER_BOARDS_PCA9685_2_REFERENCE_CLOCK_SPEED))
                self.pca9685_2_frequency = int(Config().get(Config.MOTION_CONTROLLER_BOARDS_PCA9685_2_FREQUENCY))

        except Exception as e:
            log.debug("Only 1 PCA9685 is present in the configuration")

    def activate_pca9685_boards(self):

        self.pca9685_1 = PCA9685(self.i2c, address=self.pca9685_1_address,
                                 reference_clock_speed=self.pca9685_1_reference_clock_speed)
        self.pca9685_1.frequency = self.pca9685_1_frequency

        if self.pca9685_2_address:
            self.pca9685_2 = PCA9685(self.i2c, address=self.pca9685_2_address,
                                     reference_clock_speed=self.pca9685_2_reference_clock_speed)
            self.pca9685_2.frequency = self.pca9685_2_frequency
            self.boards = 2

        log.debug(str(self.boards) + ' PCA9685 board(s) detected')

    def deactivate_pca9685_boards(self):
        try:
            self.pca9685_1.deinit()
        finally:
            try:
                if self.boards == 2:
                    self.pca9685_2.deinit()
            finally:
                self._abort_queue.put(queues.ABORT_CONTROLLER_ACTION_ABORT)

    def load_servos_configuration(self):

        # Setup servos
        self.servo_rear_shoulder_left_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_LEFT_PCA9685)
        self.servo_rear_shoulder_left_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_LEFT_CHANNEL)
        self.servo_rear_shoulder_left_min_pulse = Config().get(
            Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_LEFT_MIN_PULSE)
        self.servo_rear_shoulder_left_max_pulse = Config().get(
            Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_LEFT_MAX_PULSE)

        self.servo_rear_leg_left_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_LEFT_PCA9685)
        self.servo_rear_leg_left_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_LEFT_CHANNEL)
        self.servo_rear_leg_left_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_LEFT_MIN_PULSE)
        self.servo_rear_leg_left_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_LEFT_MAX_PULSE)

        self.servo_rear_feet_left_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_LEFT_PCA9685)
        self.servo_rear_feet_left_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_LEFT_CHANNEL)
        self.servo_rear_feet_left_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_LEFT_MIN_PULSE)
        self.servo_rear_feet_left_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_LEFT_MAX_PULSE)

        self.servo_rear_shoulder_right_pca9685 = Config().get(
            Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_RIGHT_PCA9685)
        self.servo_rear_shoulder_right_channel = Config().get(
            Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_RIGHT_CHANNEL)
        self.servo_rear_shoulder_right_min_pulse = Config().get(
            Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_RIGHT_MIN_PULSE)
        self.servo_rear_shoulder_right_max_pulse = Config().get(
            Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_RIGHT_MAX_PULSE)

        self.servo_rear_leg_right_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_RIGHT_PCA9685)
        self.servo_rear_leg_right_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_RIGHT_CHANNEL)
        self.servo_rear_leg_right_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_RIGHT_MIN_PULSE)
        self.servo_rear_leg_right_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_RIGHT_MAX_PULSE)

        self.servo_rear_feet_right_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_RIGHT_PCA9685)
        self.servo_rear_feet_right_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_RIGHT_CHANNEL)
        self.servo_rear_feet_right_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_RIGHT_MIN_PULSE)
        self.servo_rear_feet_right_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_RIGHT_MAX_PULSE)

        self.servo_front_shoulder_left_pca9685 = Config().get(
            Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_LEFT_PCA9685)
        self.servo_front_shoulder_left_channel = Config().get(
            Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_LEFT_CHANNEL)
        self.servo_front_shoulder_left_min_pulse = Config().get(
            Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_LEFT_MIN_PULSE)
        self.servo_front_shoulder_left_max_pulse = Config().get(
            Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_LEFT_MAX_PULSE)

        self.servo_front_leg_left_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_LEFT_PCA9685)
        self.servo_front_leg_left_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_LEFT_CHANNEL)
        self.servo_front_leg_left_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_LEFT_MIN_PULSE)
        self.servo_front_leg_left_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_LEFT_MAX_PULSE)

        self.servo_front_feet_left_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_LEFT_PCA9685)
        self.servo_front_feet_left_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_LEFT_CHANNEL)
        self.servo_front_feet_left_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_LEFT_MIN_PULSE)
        self.servo_front_feet_left_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_LEFT_MAX_PULSE)

        self.servo_front_shoulder_right_pca9685 = Config().get(
            Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_RIGHT_PCA9685)
        self.servo_front_shoulder_right_channel = Config().get(
            Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_RIGHT_CHANNEL)
        self.servo_front_shoulder_right_min_pulse = Config().get(
            Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_RIGHT_MIN_PULSE)
        self.servo_front_shoulder_right_max_pulse = Config().get(
            Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_RIGHT_MAX_PULSE)

        self.servo_front_leg_right_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_RIGHT_PCA9685)
        self.servo_front_leg_right_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_RIGHT_CHANNEL)
        self.servo_front_leg_right_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_RIGHT_MIN_PULSE)
        self.servo_front_leg_right_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_RIGHT_MAX_PULSE)

        self.servo_front_feet_right_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_RIGHT_PCA9685)
        self.servo_front_feet_right_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_RIGHT_CHANNEL)
        self.servo_front_feet_right_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_RIGHT_MIN_PULSE)
        self.servo_front_feet_right_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_RIGHT_MAX_PULSE)

    def activate_servos(self):

        if self.servo_rear_shoulder_left_pca9685 == 1:
            self.servo_rear_shoulder_left = servo.Servo(
                self.pca9685_1.channels[self.servo_rear_shoulder_left_channel])
        else:
            self.servo_rear_shoulder_left = servo.Servo(
                self.pca9685_2.channels[self.servo_rear_shoulder_left_channel])

        self.servo_rear_shoulder_left.set_pulse_width_range(min_pulse=servo_rear_shoulder_left_min_pulse,
                                                            max_pulse=servo_rear_shoulder_left_max_pulse)

        if servo_rear_leg_left_pca9685 == 1:
            self.servo_rear_leg_left = servo.Servo(self.pca9685_1.channels[self.servo_rear_leg_left_channel])
        else:
            self.servo_rear_leg_left = servo.Servo(self.pca9685_2.channels[self.servo_rear_leg_left_channel])

        self.servo_rear_leg_left.set_pulse_width_range(min_pulse=servo_rear_leg_left_min_pulse,
                                                       max_pulse=servo_rear_leg_left_max_pulse)

        if servo_rear_feet_left_pca9685 == 1:
            self.servo_rear_feet_left = servo.Servo(self.pca9685_1.channels[self.servo_rear_feet_left_channel])
        else:
            self.servo_rear_feet_left = servo.Servo(self.pca9685_2.channels[self.servo_rear_feet_left_channel])
        self.servo_rear_feet_left.set_pulse_width_range(min_pulse=servo_rear_feet_left_min_pulse,
                                                        max_pulse=servo_rear_feet_left_max_pulse)

        if servo_rear_shoulder_right_pca9685 == 1:
            self.servo_rear_shoulder_right = servo.Servo(
                self.pca9685_1.channels[self.servo_rear_shoulder_right_channel])
        else:
            self.servo_rear_shoulder_right = servo.Servo(
                self.pca9685_2.channels[self.servo_rear_shoulder_right_channel])
        self.servo_rear_shoulder_right.set_pulse_width_range(min_pulse=servo_rear_shoulder_right_min_pulse,
                                                             max_pulse=servo_rear_shoulder_right_max_pulse)

        if servo_rear_leg_right_pca9685 == 1:
            self.servo_rear_leg_right = servo.Servo(self.pca9685_1.channels[self.servo_rear_leg_right_channel])
        else:
            self.servo_rear_leg_right = servo.Servo(self.pca9685_2.channels[self.servo_rear_leg_right_channel])
        self.servo_rear_leg_right.set_pulse_width_range(min_pulse=servo_rear_leg_right_min_pulse,
                                                        max_pulse=servo_rear_leg_right_max_pulse)

        if servo_rear_feet_right_pca9685 == 1:
            self.servo_rear_feet_right = servo.Servo(self.pca9685_1.channels[self.servo_rear_feet_right_channel])
        else:
            self.servo_rear_feet_right = servo.Servo(self.pca9685_2.channels[self.servo_rear_feet_right_channel])
        self.servo_rear_feet_right.set_pulse_width_range(min_pulse=servo_rear_feet_right_min_pulse,
                                                         max_pulse=servo_rear_feet_right_max_pulse)

        if servo_front_shoulder_left_pca9685 == 1:
            self.servo_front_shoulder_left = servo.Servo(
                self.pca9685_1.channels[self.servo_front_shoulder_left_channel])
        else:
            self.servo_front_shoulder_left = servo.Servo(
                self.pca9685_2.channels[self.servo_front_shoulder_left_channel])
        self.servo_front_shoulder_left.set_pulse_width_range(min_pulse=servo_front_shoulder_left_min_pulse,
                                                             max_pulse=servo_front_shoulder_left_max_pulse)

        if servo_front_leg_left_pca9685 == 1:
            self.servo_front_leg_left = servo.Servo(self.pca9685_1.channels[self.servo_front_leg_left_channel])
        else:
            self.servo_front_leg_left = servo.Servo(self.pca9685_2.channels[self.servo_front_leg_left_channel])
        self.servo_front_leg_left.set_pulse_width_range(min_pulse=servo_front_leg_left_min_pulse,
                                                        max_pulse=servo_front_leg_left_max_pulse)

        if servo_front_feet_left_pca9685 == 1:
            self.servo_front_feet_left = servo.Servo(self.pca9685_1.channels[self.servo_front_feet_left_channel])
        else:
            self.servo_front_feet_left = servo.Servo(self.pca9685_2.channels[self.servo_front_feet_left_channel])
        self.servo_front_feet_left.set_pulse_width_range(min_pulse=servo_front_feet_left_min_pulse,
                                                         max_pulse=servo_front_feet_left_max_pulse)

        if servo_front_shoulder_right_pca9685 == 1:
            self.servo_front_shoulder_right = servo.Servo(
                self.pca9685_1.channels[self.servo_front_shoulder_right_channel])
        else:
            self.servo_front_shoulder_right = servo.Servo(
                self.pca9685_2.channels[self.servo_front_shoulder_right_channel])
        self.servo_front_shoulder_right.set_pulse_width_range(min_pulse=servo_front_shoulder_right_min_pulse,
                                                              max_pulse=servo_front_shoulder_right_max_pulse)

        if servo_front_leg_right_pca9685 == 1:
            self.servo_front_leg_right = servo.Servo(self.pca9685_1.channels[self.servo_front_leg_right_channel])
        else:
            self.servo_front_leg_right = servo.Servo(
                self.pca9685_2.channels[self.servo_front_leg_right_channel])
        self.servo_front_leg_right.set_pulse_width_range(min_pulse=servo_front_leg_right_min_pulse,
                                                         max_pulse=servo_front_leg_right_max_pulse)

        if servo_front_feet_right_pca9685 == 1:
            self.servo_front_feet_right = servo.Servo(self.pca9685_1.channels[self.servo_front_feet_right_channel])
        else:
            self.servo_front_feet_right = servo.Servo(self.pca9685_2.channels[self.servo_front_feet_right_channel])
        self.servo_front_feet_right.set_pulse_width_range(min_pulse=servo_front_feet_right_min_pulse,
                                                          max_pulse=servo_front_feet_right_max_pulse)

    def rest_position(self):

        self.servo_rear_shoulder_left.angle = 90
        self.servo_rear_leg_left.angle = 90
        self.servo_rear_feet_left.angle = 90

        self.servo_rear_shoulder_right.angle = 90
        self.servo_rear_leg_right.angle = 90
        self.servo_rear_feet_right.angle = 90

        self.servo_front_shoulder_left.angle = 90
        self.servo_front_leg_left.angle = 90
        self.servo_front_feet_left.angle = 90

        self.servo_front_shoulder_right.angle = 90
        self.servo_front_leg_right.angle = 90
        self.servo_front_feet_right.angle = 90

        time.sleep(0.1)

    def move_forward(self):

        self.servo_rear_shoulder_left.angle = 85
        self.servo_rear_leg_left.angle = 85
        self.servo_rear_feet_left.angle = 85

        self.servo_rear_shoulder_right.angle = 85
        self.servo_rear_leg_right.angle = 85
        self.servo_rear_feet_right.angle = 85

        self.servo_front_shoulder_left.angle = 85
        self.servo_front_leg_left.angle = 85
        self.servo_front_feet_left.angle = 85

        self.servo_front_shoulder_right.angle = 85
        self.servo_front_leg_right.angle = 85
        self.servo_front_feet_right.angle = 85

        time.sleep(0.1)
