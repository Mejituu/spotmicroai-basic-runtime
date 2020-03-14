import signal
import sys

import queue
import os
import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
import time

from spotmicroai.utilities.log import Logger
from spotmicroai.utilities.config import Config
import spotmicroai.utilities.queues as queues
from spotmicroai.utilities.general import General

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

    servo_rear_shoulder_left = None
    servo_rear_shoulder_left_pca9685 = None
    servo_rear_shoulder_left_channel = None
    servo_rear_shoulder_left_min_pulse = None
    servo_rear_shoulder_left_max_pulse = None
    servo_rear_shoulder_left_rest_angle = None

    servo_rear_leg_left = None
    servo_rear_leg_left_pca9685 = None
    servo_rear_leg_left_channel = None
    servo_rear_leg_left_min_pulse = None
    servo_rear_leg_left_max_pulse = None
    servo_rear_leg_left_rest_angle = None

    servo_rear_feet_left = None
    servo_rear_feet_left_pca9685 = None
    servo_rear_feet_left_channel = None
    servo_rear_feet_left_min_pulse = None
    servo_rear_feet_left_max_pulse = None
    servo_rear_feet_left_rest_angle = None

    servo_rear_shoulder_right = None
    servo_rear_shoulder_right_pca9685 = None
    servo_rear_shoulder_right_channel = None
    servo_rear_shoulder_right_min_pulse = None
    servo_rear_shoulder_right_max_pulse = None
    servo_rear_shoulder_right_rest_angle = None

    servo_rear_leg_right = None
    servo_rear_leg_right_pca9685 = None
    servo_rear_leg_right_channel = None
    servo_rear_leg_right_min_pulse = None
    servo_rear_leg_right_max_pulse = None
    servo_rear_leg_right_rest_angle = None

    servo_rear_feet_right = None
    servo_rear_feet_right_pca9685 = None
    servo_rear_feet_right_channel = None
    servo_rear_feet_right_min_pulse = None
    servo_rear_feet_right_max_pulse = None
    servo_rear_feet_right_rest_angle = None

    servo_front_shoulder_left = None
    servo_front_shoulder_left_pca9685 = None
    servo_front_shoulder_left_channel = None
    servo_front_shoulder_left_min_pulse = None
    servo_front_shoulder_left_max_pulse = None
    servo_front_shoulder_left_rest_angle = None

    servo_front_leg_left = None
    servo_front_leg_left_pca9685 = None
    servo_front_leg_left_channel = None
    servo_front_leg_left_min_pulse = None
    servo_front_leg_left_max_pulse = None
    servo_front_leg_left_rest_angle = None

    servo_front_feet_left = None
    servo_front_feet_left_pca9685 = None
    servo_front_feet_left_channel = None
    servo_front_feet_left_min_pulse = None
    servo_front_feet_left_max_pulse = None
    servo_front_feet_left_rest_angle = None

    servo_front_shoulder_right = None
    servo_front_shoulder_right_pca9685 = None
    servo_front_shoulder_right_channel = None
    servo_front_shoulder_right_min_pulse = None
    servo_front_shoulder_right_max_pulse = None
    servo_front_shoulder_right_rest_angle = None

    servo_front_leg_right = None
    servo_front_leg_right_pca9685 = None
    servo_front_leg_right_channel = None
    servo_front_leg_right_min_pulse = None
    servo_front_leg_right_max_pulse = None
    servo_front_leg_right_rest_angle = None

    servo_front_feet_right = None
    servo_front_feet_right_pca9685 = None
    servo_front_feet_right_channel = None
    servo_front_feet_right_min_pulse = None
    servo_front_feet_right_max_pulse = None
    servo_front_feet_right_rest_angle = None

    def __init__(self, communication_queues):

        try:

            log.debug('Starting controller...')

            signal.signal(signal.SIGINT, self.exit_gracefully)
            signal.signal(signal.SIGTERM, self.exit_gracefully)

            self.i2c = busio.I2C(SCL, SDA)
            self.load_pca9685_boards_configuration()
            self.load_servos_configuration()

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

                event = self._motion_queue.get(block=True, timeout=60)

                # log.debug(event)

                if event['start']:
                    if self.is_activated:
                        self.rest_position()
                        time.sleep(0.5)
                        self.deactivate_pca9685_boards()
                        self._abort_queue.put(queues.ABORT_CONTROLLER_ACTION_ABORT)
                    else:
                        self._abort_queue.put(queues.ABORT_CONTROLLER_ACTION_ACTIVATE)
                        self.activate_pca9685_boards()
                        self.activate_servos()
                        self.rest_position()

                if not self.is_activated:
                    log.info('Press START/OPTIONS to enable the servos')
                    continue

                if event['a']:
                    self.rest_position()

                if event['hat0y']:
                    self.body_move_body_up_and_down(event['hat0y'])

                if event['hat0x']:
                    self.body_move_body_left_right(event['hat0x'])

                if event['y']:
                    self.walk_forward()

                if event['ly']:
                    pass

                if event['lx']:
                    pass

                if event['ry']:
                    self.body_move_body_up_and_down_analog(event['ry'])

                if event['rx']:
                    self.body_move_body_left_right_analog(event['rx'])

                if event['hat0x'] and event['tl2']:
                    pass

                self.move()

            except queue.Empty as e:
                log.info('Inactivity lasted 60 seconds, shutting down the servos, '
                         'press start to reactivate')
                if self.is_activated:
                    self.rest_position()
                    time.sleep(0.5)
                    self.deactivate_pca9685_boards()

            except Exception as e:
                log.error('Unknown problem while processing the queue of the motion controller')
                log.error(' - Most likely a servo is not able to get to the assigned position')

    def load_pca9685_boards_configuration(self):
        self.pca9685_1_address = int(Config().get(Config.MOTION_CONTROLLER_BOARDS_PCA9685_1_ADDRESS), 0)
        self.pca9685_1_reference_clock_speed = int(Config().get(Config.MOTION_CONTROLLER_BOARDS_PCA9685_1_REFERENCE_CLOCK_SPEED))
        self.pca9685_1_frequency = int(Config().get(Config.MOTION_CONTROLLER_BOARDS_PCA9685_1_FREQUENCY))

        self.pca9685_2_address = False
        try:
            self.pca9685_2_address = int(Config().get(Config.MOTION_CONTROLLER_BOARDS_PCA9685_2_ADDRESS), 0)

            if self.pca9685_2_address:
                self.pca9685_2_reference_clock_speed = int(Config().get(Config.MOTION_CONTROLLER_BOARDS_PCA9685_2_REFERENCE_CLOCK_SPEED))
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

        self.is_activated = True
        log.debug(str(self.boards) + ' PCA9685 board(s) activated')

    def deactivate_pca9685_boards(self):

        try:
            if self.pca9685_1:
                self.pca9685_1.deinit()
        finally:
            try:
                if self.boards == 2 and self.pca9685_2:
                    self.pca9685_2.deinit()
            finally:
                # self._abort_queue.put(queues.ABORT_CONTROLLER_ACTION_ABORT)
                self.is_activated = False

        log.debug(str(self.boards) + ' PCA9685 board(s) deactivated')

    def load_servos_configuration(self):

        self.servo_rear_shoulder_left_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_LEFT_PCA9685)
        self.servo_rear_shoulder_left_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_LEFT_CHANNEL)
        self.servo_rear_shoulder_left_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_LEFT_MIN_PULSE)
        self.servo_rear_shoulder_left_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_LEFT_MAX_PULSE)
        self.servo_rear_shoulder_left_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_LEFT_REST_ANGLE)

        self.servo_rear_leg_left_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_LEFT_PCA9685)
        self.servo_rear_leg_left_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_LEFT_CHANNEL)
        self.servo_rear_leg_left_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_LEFT_MIN_PULSE)
        self.servo_rear_leg_left_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_LEFT_MAX_PULSE)
        self.servo_rear_leg_left_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_LEFT_REST_ANGLE)

        self.servo_rear_feet_left_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_LEFT_PCA9685)
        self.servo_rear_feet_left_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_LEFT_CHANNEL)
        self.servo_rear_feet_left_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_LEFT_MIN_PULSE)
        self.servo_rear_feet_left_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_LEFT_MAX_PULSE)
        self.servo_rear_feet_left_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_LEFT_REST_ANGLE)

        self.servo_rear_shoulder_right_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_RIGHT_PCA9685)
        self.servo_rear_shoulder_right_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_RIGHT_CHANNEL)
        self.servo_rear_shoulder_right_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_RIGHT_MIN_PULSE)
        self.servo_rear_shoulder_right_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_RIGHT_MAX_PULSE)
        self.servo_rear_shoulder_right_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_RIGHT_REST_ANGLE)

        self.servo_rear_leg_right_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_RIGHT_PCA9685)
        self.servo_rear_leg_right_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_RIGHT_CHANNEL)
        self.servo_rear_leg_right_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_RIGHT_MIN_PULSE)
        self.servo_rear_leg_right_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_RIGHT_MAX_PULSE)
        self.servo_rear_leg_right_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_RIGHT_REST_ANGLE)

        self.servo_rear_feet_right_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_RIGHT_PCA9685)
        self.servo_rear_feet_right_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_RIGHT_CHANNEL)
        self.servo_rear_feet_right_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_RIGHT_MIN_PULSE)
        self.servo_rear_feet_right_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_RIGHT_MAX_PULSE)
        self.servo_rear_feet_right_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_RIGHT_REST_ANGLE)

        self.servo_front_shoulder_left_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_LEFT_PCA9685)
        self.servo_front_shoulder_left_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_LEFT_CHANNEL)
        self.servo_front_shoulder_left_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_LEFT_MIN_PULSE)
        self.servo_front_shoulder_left_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_LEFT_MAX_PULSE)
        self.servo_front_shoulder_left_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_LEFT_REST_ANGLE)

        self.servo_front_leg_left_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_LEFT_PCA9685)
        self.servo_front_leg_left_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_LEFT_CHANNEL)
        self.servo_front_leg_left_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_LEFT_MIN_PULSE)
        self.servo_front_leg_left_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_LEFT_MAX_PULSE)
        self.servo_front_leg_left_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_LEFT_REST_ANGLE)

        self.servo_front_feet_left_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_LEFT_PCA9685)
        self.servo_front_feet_left_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_LEFT_CHANNEL)
        self.servo_front_feet_left_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_LEFT_MIN_PULSE)
        self.servo_front_feet_left_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_LEFT_MAX_PULSE)
        self.servo_front_feet_left_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_LEFT_REST_ANGLE)

        self.servo_front_shoulder_right_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_RIGHT_PCA9685)
        self.servo_front_shoulder_right_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_RIGHT_CHANNEL)
        self.servo_front_shoulder_right_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_RIGHT_MIN_PULSE)
        self.servo_front_shoulder_right_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_RIGHT_MAX_PULSE)
        self.servo_front_shoulder_right_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_RIGHT_REST_ANGLE)

        self.servo_front_leg_right_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_RIGHT_PCA9685)
        self.servo_front_leg_right_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_RIGHT_CHANNEL)
        self.servo_front_leg_right_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_RIGHT_MIN_PULSE)
        self.servo_front_leg_right_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_RIGHT_MAX_PULSE)
        self.servo_front_leg_right_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_RIGHT_REST_ANGLE)

        self.servo_front_feet_right_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_RIGHT_PCA9685)
        self.servo_front_feet_right_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_RIGHT_CHANNEL)
        self.servo_front_feet_right_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_RIGHT_MIN_PULSE)
        self.servo_front_feet_right_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_RIGHT_MAX_PULSE)
        self.servo_front_feet_right_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_RIGHT_REST_ANGLE)

    def activate_servos(self):

        if self.servo_rear_shoulder_left_pca9685 == 1:
            self.servo_rear_shoulder_left = servo.Servo(self.pca9685_1.channels[self.servo_rear_shoulder_left_channel])
        else:
            self.servo_rear_shoulder_left = servo.Servo(self.pca9685_2.channels[self.servo_rear_shoulder_left_channel])
        self.servo_rear_shoulder_left.set_pulse_width_range(min_pulse=self.servo_rear_shoulder_left_min_pulse, max_pulse=self.servo_rear_shoulder_left_max_pulse)

        if self.servo_rear_leg_left_pca9685 == 1:
            self.servo_rear_leg_left = servo.Servo(self.pca9685_1.channels[self.servo_rear_leg_left_channel])
        else:
            self.servo_rear_leg_left = servo.Servo(self.pca9685_2.channels[self.servo_rear_leg_left_channel])
        self.servo_rear_leg_left.set_pulse_width_range(min_pulse=self.servo_rear_leg_left_min_pulse, max_pulse=self.servo_rear_leg_left_max_pulse)

        if self.servo_rear_feet_left_pca9685 == 1:
            self.servo_rear_feet_left = servo.Servo(self.pca9685_1.channels[self.servo_rear_feet_left_channel])
        else:
            self.servo_rear_feet_left = servo.Servo(self.pca9685_2.channels[self.servo_rear_feet_left_channel])
        self.servo_rear_feet_left.set_pulse_width_range(min_pulse=self.servo_rear_feet_left_min_pulse, max_pulse=self.servo_rear_feet_left_max_pulse)

        if self.servo_rear_shoulder_right_pca9685 == 1:
            self.servo_rear_shoulder_right = servo.Servo(self.pca9685_1.channels[self.servo_rear_shoulder_right_channel])
        else:
            self.servo_rear_shoulder_right = servo.Servo(self.pca9685_2.channels[self.servo_rear_shoulder_right_channel])
        self.servo_rear_shoulder_right.set_pulse_width_range(min_pulse=self.servo_rear_shoulder_right_min_pulse, max_pulse=self.servo_rear_shoulder_right_max_pulse)

        if self.servo_rear_leg_right_pca9685 == 1:
            self.servo_rear_leg_right = servo.Servo(self.pca9685_1.channels[self.servo_rear_leg_right_channel])
        else:
            self.servo_rear_leg_right = servo.Servo(self.pca9685_2.channels[self.servo_rear_leg_right_channel])
        self.servo_rear_leg_right.set_pulse_width_range(min_pulse=self.servo_rear_leg_right_min_pulse, max_pulse=self.servo_rear_leg_right_max_pulse)

        if self.servo_rear_feet_right_pca9685 == 1:
            self.servo_rear_feet_right = servo.Servo(self.pca9685_1.channels[self.servo_rear_feet_right_channel])
        else:
            self.servo_rear_feet_right = servo.Servo(self.pca9685_2.channels[self.servo_rear_feet_right_channel])
        self.servo_rear_feet_right.set_pulse_width_range(min_pulse=self.servo_rear_feet_right_min_pulse, max_pulse=self.servo_rear_feet_right_max_pulse)

        if self.servo_front_shoulder_left_pca9685 == 1:
            self.servo_front_shoulder_left = servo.Servo(self.pca9685_1.channels[self.servo_front_shoulder_left_channel])
        else:
            self.servo_front_shoulder_left = servo.Servo(self.pca9685_2.channels[self.servo_front_shoulder_left_channel])
        self.servo_front_shoulder_left.set_pulse_width_range(min_pulse=self.servo_front_shoulder_left_min_pulse, max_pulse=self.servo_front_shoulder_left_max_pulse)

        if self.servo_front_leg_left_pca9685 == 1:
            self.servo_front_leg_left = servo.Servo(self.pca9685_1.channels[self.servo_front_leg_left_channel])
        else:
            self.servo_front_leg_left = servo.Servo(self.pca9685_2.channels[self.servo_front_leg_left_channel])
        self.servo_front_leg_left.set_pulse_width_range(min_pulse=self.servo_front_leg_left_min_pulse, max_pulse=self.servo_front_leg_left_max_pulse)

        if self.servo_front_feet_left_pca9685 == 1:
            self.servo_front_feet_left = servo.Servo(self.pca9685_1.channels[self.servo_front_feet_left_channel])
        else:
            self.servo_front_feet_left = servo.Servo(self.pca9685_2.channels[self.servo_front_feet_left_channel])
        self.servo_front_feet_left.set_pulse_width_range(min_pulse=self.servo_front_feet_left_min_pulse, max_pulse=self.servo_front_feet_left_max_pulse)

        if self.servo_front_shoulder_right_pca9685 == 1:
            self.servo_front_shoulder_right = servo.Servo(self.pca9685_1.channels[self.servo_front_shoulder_right_channel])
        else:
            self.servo_front_shoulder_right = servo.Servo(
                self.pca9685_2.channels[self.servo_front_shoulder_right_channel])
        self.servo_front_shoulder_right.set_pulse_width_range(min_pulse=self.servo_front_shoulder_right_min_pulse, max_pulse=self.servo_front_shoulder_right_max_pulse)

        if self.servo_front_leg_right_pca9685 == 1:
            self.servo_front_leg_right = servo.Servo(self.pca9685_1.channels[self.servo_front_leg_right_channel])
        else:
            self.servo_front_leg_right = servo.Servo(
                self.pca9685_2.channels[self.servo_front_leg_right_channel])
        self.servo_front_leg_right.set_pulse_width_range(min_pulse=self.servo_front_leg_right_min_pulse, max_pulse=self.servo_front_leg_right_max_pulse)

        if self.servo_front_feet_right_pca9685 == 1:
            self.servo_front_feet_right = servo.Servo(self.pca9685_1.channels[self.servo_front_feet_right_channel])
        else:
            self.servo_front_feet_right = servo.Servo(self.pca9685_2.channels[self.servo_front_feet_right_channel])
        self.servo_front_feet_right.set_pulse_width_range(min_pulse=self.servo_front_feet_right_min_pulse, max_pulse=self.servo_front_feet_right_max_pulse)

    def move(self):

        try:
            self.servo_rear_shoulder_left.angle = self.servo_rear_shoulder_left_rest_angle
        except ValueError as e:
            log.error('Impossible servo_rear_shoulder_left angle requested')

        try:
            self.servo_rear_leg_left.angle = self.servo_rear_leg_left_rest_angle
        except ValueError as e:
            log.error('Impossible servo_rear_leg_left angle requested')

        try:
            self.servo_rear_feet_left.angle = self.servo_rear_feet_left_rest_angle
        except ValueError as e:
            log.error('Impossible servo_rear_feet_left angle requested')

        try:
            self.servo_rear_shoulder_right.angle = self.servo_rear_shoulder_right_rest_angle
        except ValueError as e:
            log.error('Impossible servo_rear_shoulder_right angle requested')

        try:
            self.servo_rear_leg_right.angle = self.servo_rear_leg_right_rest_angle
        except ValueError as e:
            log.error('Impossible servo_rear_leg_right angle requested')

        try:
            self.servo_rear_feet_right.angle = self.servo_rear_feet_right_rest_angle
        except ValueError as e:
            log.error('Impossible servo_rear_feet_right angle requested')

        try:
            self.servo_front_shoulder_left.angle = self.servo_front_shoulder_left_rest_angle
        except ValueError as e:
            log.error('Impossible servo_front_shoulder_left angle requested')

        try:
            self.servo_front_leg_left.angle = self.servo_front_leg_left_rest_angle
        except ValueError as e:
            log.error('Impossible servo_front_leg_left angle requested')

        try:
            self.servo_front_feet_left.angle = self.servo_front_feet_left_rest_angle
        except ValueError as e:
            log.error('Impossible servo_front_feet_left angle requested')

        try:
            self.servo_front_shoulder_right.angle = self.servo_front_shoulder_right_rest_angle
        except ValueError as e:
            log.error('Impossible servo_front_shoulder_right angle requested')

        try:
            self.servo_front_leg_right.angle = self.servo_front_leg_right_rest_angle
        except ValueError as e:
            log.error('Impossible servo_front_leg_right angle requested')

        try:
            self.servo_front_feet_right.angle = self.servo_front_feet_right_rest_angle
        except ValueError as e:
            log.error('Impossible servo_front_feet_right angle requested')

    def rest_position(self):

        self.servo_rear_shoulder_left_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_LEFT_REST_ANGLE)
        self.servo_rear_leg_left_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_LEFT_REST_ANGLE)
        self.servo_rear_feet_left_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_LEFT_REST_ANGLE)
        self.servo_rear_shoulder_right_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_RIGHT_REST_ANGLE)
        self.servo_rear_leg_right_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_RIGHT_REST_ANGLE)
        self.servo_rear_feet_right_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_RIGHT_REST_ANGLE)
        self.servo_front_shoulder_left_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_LEFT_REST_ANGLE)
        self.servo_front_leg_left_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_LEFT_REST_ANGLE)
        self.servo_front_feet_left_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_LEFT_REST_ANGLE)
        self.servo_front_shoulder_right_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_RIGHT_REST_ANGLE)
        self.servo_front_leg_right_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_RIGHT_REST_ANGLE)
        self.servo_front_feet_right_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_RIGHT_REST_ANGLE)

    def body_move_body_up_and_down(self, raw_value):

        range = 10
        range2 = 15

        if raw_value < 0:
            self.servo_rear_leg_left_rest_angle -= range
            self.servo_rear_feet_left_rest_angle += range2
            self.servo_rear_leg_right_rest_angle += range
            self.servo_rear_feet_right_rest_angle -= range2
            self.servo_front_leg_left_rest_angle -= range
            self.servo_front_feet_left_rest_angle += range2
            self.servo_front_leg_right_rest_angle += range
            self.servo_front_feet_right_rest_angle -= range2

        elif raw_value > 0:
            self.servo_rear_leg_left_rest_angle += range
            self.servo_rear_feet_left_rest_angle -= range2
            self.servo_rear_leg_right_rest_angle -= range
            self.servo_rear_feet_right_rest_angle += range2
            self.servo_front_leg_left_rest_angle += range
            self.servo_front_feet_left_rest_angle -= range2
            self.servo_front_leg_right_rest_angle -= range
            self.servo_front_feet_right_rest_angle += range2

        else:
            self.rest_position()

        print(str(self.servo_rear_leg_left_rest_angle) + ', ' + str(self.servo_rear_feet_left_rest_angle) + ', ' + str(self.servo_rear_leg_right_rest_angle) + ', ' + str(self.servo_rear_feet_right_rest_angle) + ', ' + str(self.servo_front_leg_left_rest_angle) + ', ' + str(self.servo_front_feet_left_rest_angle) + ', ' + str(self.servo_front_leg_right_rest_angle) + ', ' + str(self.servo_front_feet_right_rest_angle))

    def body_move_body_up_and_down_analog(self, raw_value):

        servo_rear_leg_left_max_angle = 38
        servo_rear_feet_left_max_angle = 70
        servo_rear_leg_right_max_angle = 126
        servo_rear_feet_right_max_angle = 102
        servo_front_leg_left_max_angle = 57
        servo_front_feet_left_max_angle = 85
        servo_front_leg_right_max_angle = 130
        servo_front_feet_right_max_angle = 120

        delta_rear_leg_left = int(General().maprange((1, -1), (Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_LEFT_REST_ANGLE), servo_rear_leg_left_max_angle), raw_value))
        delta_rear_feet_left = int(General().maprange((1, -1), (Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_LEFT_REST_ANGLE), servo_rear_feet_left_max_angle), raw_value))
        delta_rear_leg_right = int(General().maprange((1, -1), (Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_RIGHT_REST_ANGLE), servo_rear_leg_right_max_angle), raw_value))
        delta_rear_feet_right = int(General().maprange((1, -1), (Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_RIGHT_REST_ANGLE), servo_rear_feet_right_max_angle), raw_value))
        delta_front_leg_left = int(General().maprange((1, -1), (Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_LEFT_REST_ANGLE), servo_front_leg_left_max_angle), raw_value))
        delta_front_feet_left = int(General().maprange((1, -1), (Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_LEFT_REST_ANGLE), servo_front_feet_left_max_angle), raw_value))
        delta_front_leg_right = int(General().maprange((1, -1), (Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_RIGHT_REST_ANGLE), servo_front_leg_right_max_angle), raw_value))
        delta_front_feet_right = int(General().maprange((1, -1), (Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_RIGHT_REST_ANGLE), servo_front_feet_right_max_angle), raw_value))

        self.servo_rear_leg_left_rest_angle = delta_rear_leg_left
        self.servo_rear_feet_left_rest_angle = delta_rear_feet_left
        self.servo_rear_leg_right_rest_angle = delta_rear_leg_right
        self.servo_rear_feet_right_rest_angle = delta_rear_feet_right
        self.servo_front_leg_left_rest_angle = delta_front_leg_left
        self.servo_front_feet_left_rest_angle = delta_front_feet_left
        self.servo_front_leg_right_rest_angle = delta_front_leg_right
        self.servo_front_feet_right_rest_angle = delta_front_feet_right

    def body_move_body_left_right(self, raw_value):

        range = 5

        if raw_value < 0:
            self.servo_rear_shoulder_left_rest_angle -= range
            self.servo_rear_shoulder_right_rest_angle -= range
            self.servo_front_shoulder_left_rest_angle += range
            self.servo_front_shoulder_right_rest_angle += range

        elif raw_value > 0:
            self.servo_rear_shoulder_left_rest_angle += range
            self.servo_rear_shoulder_right_rest_angle += range
            self.servo_front_shoulder_left_rest_angle -= range
            self.servo_front_shoulder_right_rest_angle -= range

        else:
            self.rest_position()

    def body_move_body_left_right_analog(self, raw_value):

        delta_a = int(General().maprange((-1, 1), (30, 150), raw_value))
        delta_b = int(General().maprange((-1, 1), (150, 30), raw_value))

        self.servo_rear_shoulder_left_rest_angle = delta_a
        self.servo_rear_shoulder_right_rest_angle = delta_a
        self.servo_front_shoulder_left_rest_angle = delta_b
        self.servo_front_shoulder_right_rest_angle = delta_b

    def walk_forward(self):

        # self.rest_position()
        # time.sleep(1)

        self.servo_front_shoulder_right_rest_angle += 20
        time.sleep(1)

        self.servo_front_leg_right_rest_angle += 40
        time.sleep(1)

        self.servo_front_feet_right_rest_angle -= 20
        time.sleep(1)

        self.servo_front_shoulder_right_rest_angle -= 20
        time.sleep(1)

        self.servo_front_leg_right_rest_angle -= 40
        time.sleep(1)
