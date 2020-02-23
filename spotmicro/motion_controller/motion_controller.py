import signal
import sys

import queue

import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

from spotmicro.utilities.log import Logger
from spotmicro.utilities.config import Config

log = Logger().setup_logger('Motion controller')


class MotionController:
    boards = 1

    def __init__(self, communication_queues):

        try:

            log.debug('Starting controller...')

            signal.signal(signal.SIGINT, self.exit_gracefully)
            signal.signal(signal.SIGTERM, self.exit_gracefully)

            # Setup I2C PCA9685
            self.i2c = busio.I2C(SCL, SDA)

            pca9685_1_address = int(
                Config().get('motion_controller[*].boards[*].pca9685_1[*].address | [0] | [0] | [0]'), 0)
            pca9685_1_reference_clock_speed = int(Config().get(
                'motion_controller[*].boards[*].pca9685_1[*].reference_clock_speed | [0] | [0] | [0]'))
            pca9685_1_frequency = int(
                Config().get('motion_controller[*].boards[*].pca9685_1[*].frequency | [0] | [0] | [0]'))

            self.pca9685_1 = PCA9685(self.i2c, address=pca9685_1_address,
                                     reference_clock_speed=pca9685_1_reference_clock_speed)
            self.pca9685_1.frequency = pca9685_1_frequency

            pca9685_2_address = int(
                Config().get('motion_controller[*].boards[*].pca9685_2[*].address | [0] | [0] | [0]'), 0)
            if pca9685_2_address:
                pca9685_2_reference_clock_speed = int(Config().get(
                    'motion_controller[*].boards[*].pca9685_2[*].reference_clock_speed | [0] | [0] | [0]'))
                pca9685_2_frequency = int(Config().get(
                    'motion_controller[*].boards[*].pca9685_2[*].frequency | [0] | [0] | [0]'))

                self.pca9685_2 = PCA9685(self.i2c, address=pca9685_2_address,
                                         reference_clock_speed=pca9685_2_reference_clock_speed)
                self.pca9685_2.frequency = pca9685_2_frequency

                self.boards = 2
                log.info("2 PCA9685 board detected")
            else:
                log.info("1 PCA9685 board detected")

            # Setup servos
            servo_rear_shoulder_left_pca9685 = Config().get(
                'motion_controller[*].servos[*].rear_shoulder_left[*].pca9685 | [0] | [0] | [0]')
            servo_rear_shoulder_left_channel = Config().get(
                'motion_controller[*].servos[*].rear_shoulder_left[*].channel | [0] | [0] | [0]')
            servo_rear_shoulder_left_min_pulse = Config().get(
                'motion_controller[*].servos[*].rear_shoulder_left[*].min_pulse | [0] | [0] | [0]')
            servo_rear_shoulder_left_max_pulse = Config().get(
                'motion_controller[*].servos[*].rear_shoulder_left[*].max_pulse | [0] | [0] | [0]')

            if servo_rear_shoulder_left_pca9685 == 1:
                self.servo_rear_shoulder_left = servo.Servo(self.pca9685_1.channels[servo_rear_shoulder_left_channel])
            else:
                self.servo_rear_shoulder_left = servo.Servo(self.pca9685_2.channels[servo_rear_shoulder_left_channel])

            self.servo_rear_shoulder_left.set_pulse_width_range(min_pulse=servo_rear_shoulder_left_min_pulse,
                                                                max_pulse=servo_rear_shoulder_left_max_pulse)

            servo_rear_leg_left_pca9685 = Config().get(
                'motion_controller[*].servos[*].rear_leg_left[*].pca9685 | [0] | [0] | [0]')
            servo_rear_leg_left_channel = Config().get(
                'motion_controller[*].servos[*].rear_leg_left[*].channel | [0] | [0] | [0]')
            servo_rear_leg_left_min_pulse = Config().get(
                'motion_controller[*].servos[*].rear_leg_left[*].min_pulse | [0] | [0] | [0]')
            servo_rear_leg_left_max_pulse = Config().get(
                'motion_controller[*].servos[*].rear_leg_left[*].max_pulse | [0] | [0] | [0]')

            if servo_rear_leg_left_pca9685 == 1:
                self.servo_rear_leg_left = servo.Servo(self.pca9685_1.channels[servo_rear_leg_left_channel])
            else:
                self.servo_rear_leg_left = servo.Servo(self.pca9685_2.channels[servo_rear_leg_left_channel])

            self.servo_rear_leg_left.set_pulse_width_range(min_pulse=servo_rear_leg_left_min_pulse,
                                                           max_pulse=servo_rear_leg_left_max_pulse)

            servo_rear_feet_left_pca9685 = Config().get(
                'motion_controller[*].servos[*].rear_feet_left[*].pca9685 | [0] | [0] | [0]')
            servo_rear_feet_left_channel = Config().get(
                'motion_controller[*].servos[*].rear_feet_left[*].channel | [0] | [0] | [0]')
            servo_rear_feet_left_min_pulse = Config().get(
                'motion_controller[*].servos[*].rear_feet_left[*].min_pulse | [0] | [0] | [0]')
            servo_rear_feet_left_max_pulse = Config().get(
                'motion_controller[*].servos[*].rear_feet_left[*].max_pulse | [0] | [0] | [0]')

            if servo_rear_feet_left_pca9685 == 1:
                self.servo_rear_feet_left = servo.Servo(self.pca9685_1.channels[servo_rear_feet_left_channel])
            else:
                self.servo_rear_feet_left = servo.Servo(self.pca9685_2.channels[servo_rear_feet_left_channel])
            self.servo_rear_feet_left.set_pulse_width_range(min_pulse=servo_rear_feet_left_min_pulse,
                                                            max_pulse=servo_rear_feet_left_max_pulse)

            servo_rear_shoulder_right_pca9685 = Config().get(
                'motion_controller[*].servos[*].rear_shoulder_right[*].pca9685 | [0] | [0] | [0]')
            servo_rear_shoulder_right_channel = Config().get(
                'motion_controller[*].servos[*].rear_shoulder_right[*].channel | [0] | [0] | [0]')
            servo_rear_shoulder_right_min_pulse = Config().get(
                'motion_controller[*].servos[*].rear_shoulder_right[*].min_pulse | [0] | [0] | [0]')
            servo_rear_shoulder_right_max_pulse = Config().get(
                'motion_controller[*].servos[*].rear_shoulder_right[*].max_pulse | [0] | [0] | [0]')

            if servo_rear_shoulder_right_pca9685 == 1:
                self.servo_rear_shoulder_right = servo.Servo(self.pca9685_1.channels[servo_rear_shoulder_right_channel])
            else:
                self.servo_rear_shoulder_right = servo.Servo(self.pca9685_2.channels[servo_rear_shoulder_right_channel])
            self.servo_rear_shoulder_right.set_pulse_width_range(min_pulse=servo_rear_shoulder_right_min_pulse,
                                                                 max_pulse=servo_rear_shoulder_right_max_pulse)

            servo_rear_leg_right_pca9685 = Config().get(
                'motion_controller[*].servos[*].rear_leg_right[*].pca9685 | [0] | [0] | [0]')
            servo_rear_leg_right_channel = Config().get(
                'motion_controller[*].servos[*].rear_leg_right[*].channel | [0] | [0] | [0]')
            servo_rear_leg_right_min_pulse = Config().get(
                'motion_controller[*].servos[*].rear_leg_right[*].min_pulse | [0] | [0] | [0]')
            servo_rear_leg_right_max_pulse = Config().get(
                'motion_controller[*].servos[*].rear_leg_right[*].max_pulse | [0] | [0] | [0]')

            if servo_rear_leg_right_pca9685 == 1:
                self.servo_rear_leg_right = servo.Servo(self.pca9685_1.channels[servo_rear_leg_right_channel])
            else:
                self.servo_rear_leg_right = servo.Servo(self.pca9685_2.channels[servo_rear_leg_right_channel])
            self.servo_rear_leg_right.set_pulse_width_range(min_pulse=servo_rear_leg_right_min_pulse,
                                                            max_pulse=servo_rear_leg_right_max_pulse)

            servo_rear_feet_right_pca9685 = Config().get(
                'motion_controller[*].servos[*].rear_feet_right[*].pca9685 | [0] | [0] | [0]')
            servo_rear_feet_right_channel = Config().get(
                'motion_controller[*].servos[*].rear_feet_right[*].channel | [0] | [0] | [0]')
            servo_rear_feet_right_min_pulse = Config().get(
                'motion_controller[*].servos[*].rear_feet_right[*].min_pulse | [0] | [0] | [0]')
            servo_rear_feet_right_max_pulse = Config().get(
                'motion_controller[*].servos[*].rear_feet_right[*].max_pulse | [0] | [0] | [0]')

            if servo_rear_feet_right_pca9685 == 1:
                self.servo_rear_feet_right = servo.Servo(self.pca9685_1.channels[servo_rear_feet_right_channel])
            else:
                self.servo_rear_feet_right = servo.Servo(self.pca9685_2.channels[servo_rear_feet_right_channel])
            self.servo_rear_feet_right.set_pulse_width_range(min_pulse=servo_rear_feet_right_min_pulse,
                                                             max_pulse=servo_rear_feet_right_max_pulse)

            servo_front_shoulder_left_pca9685 = Config().get(
                'motion_controller[*].servos[*].front_shoulder_left[*].pca9685 | [0] | [0] | [0]')
            servo_front_shoulder_left_channel = Config().get(
                'motion_controller[*].servos[*].front_shoulder_left[*].channel | [0] | [0] | [0]')
            servo_front_shoulder_left_min_pulse = Config().get(
                'motion_controller[*].servos[*].front_shoulder_left[*].min_pulse | [0] | [0] | [0]')
            servo_front_shoulder_left_max_pulse = Config().get(
                'motion_controller[*].servos[*].front_shoulder_left[*].max_pulse | [0] | [0] | [0]')

            if servo_front_shoulder_left_pca9685 == 1:
                self.servo_front_shoulder_left = servo.Servo(self.pca9685_1.channels[servo_front_shoulder_left_channel])
            else:
                self.servo_front_shoulder_left = servo.Servo(self.pca9685_2.channels[servo_front_shoulder_left_channel])
            self.servo_front_shoulder_left.set_pulse_width_range(min_pulse=servo_front_shoulder_left_min_pulse,
                                                                 max_pulse=servo_front_shoulder_left_max_pulse)

            servo_front_leg_left_pca9685 = Config().get(
                'motion_controller[*].servos[*].front_leg_left[*].pca9685 | [0] | [0] | [0]')
            servo_front_leg_left_channel = Config().get(
                'motion_controller[*].servos[*].front_leg_left[*].channel | [0] | [0] | [0]')
            servo_front_leg_left_min_pulse = Config().get(
                'motion_controller[*].servos[*].front_leg_left[*].min_pulse | [0] | [0] | [0]')
            servo_front_leg_left_max_pulse = Config().get(
                'motion_controller[*].servos[*].front_leg_left[*].max_pulse | [0] | [0] | [0]')

            if servo_front_leg_left_pca9685 == 1:
                self.servo_front_leg_left = servo.Servo(self.pca9685_1.channels[servo_front_leg_left_channel])
            else:
                self.servo_front_leg_left = servo.Servo(self.pca9685_2.channels[servo_front_leg_left_channel])
            self.servo_front_leg_left.set_pulse_width_range(min_pulse=servo_front_leg_left_min_pulse,
                                                            max_pulse=servo_front_leg_left_max_pulse)

            servo_front_feet_left_pca9685 = Config().get(
                'motion_controller[*].servos[*].front_feet_left[*].pca9685 | [0] | [0] | [0]')
            servo_front_feet_left_channel = Config().get(
                'motion_controller[*].servos[*].front_feet_left[*].channel | [0] | [0] | [0]')
            servo_front_feet_left_min_pulse = Config().get(
                'motion_controller[*].servos[*].front_feet_left[*].min_pulse | [0] | [0] | [0]')
            servo_front_feet_left_max_pulse = Config().get(
                'motion_controller[*].servos[*].front_feet_left[*].max_pulse | [0] | [0] | [0]')

            if servo_front_feet_left_pca9685 == 1:
                self.servo_front_feet_left = servo.Servo(self.pca9685_1.channels[servo_front_feet_left_channel])
            else:
                self.servo_front_feet_left = servo.Servo(self.pca9685_2.channels[servo_front_feet_left_channel])
            self.servo_front_feet_left.set_pulse_width_range(min_pulse=servo_front_feet_left_min_pulse,
                                                             max_pulse=servo_front_feet_left_max_pulse)

            servo_front_shoulder_right_pca9685 = Config().get(
                'motion_controller[*].servos[*].front_shoulder_right[*].pca9685 | [0] | [0] | [0]')
            servo_front_shoulder_right_channel = Config().get(
                'motion_controller[*].servos[*].front_shoulder_right[*].channel | [0] | [0] | [0]')
            servo_front_shoulder_right_min_pulse = Config().get(
                'motion_controller[*].servos[*].front_shoulder_right[*].min_pulse | [0] | [0] | [0]')
            servo_front_shoulder_right_max_pulse = Config().get(
                'motion_controller[*].servos[*].front_shoulder_right[*].max_pulse | [0] | [0] | [0]')

            if servo_front_shoulder_right_pca9685 == 1:
                self.servo_front_shoulder_right = servo.Servo(
                    self.pca9685_1.channels[servo_front_shoulder_right_channel])
            else:
                self.servo_front_shoulder_right = servo.Servo(
                    self.pca9685_2.channels[servo_front_shoulder_right_channel])
            self.servo_front_shoulder_right.set_pulse_width_range(min_pulse=servo_front_shoulder_right_min_pulse,
                                                                  max_pulse=servo_front_shoulder_right_max_pulse)

            servo_front_leg_right_pca9685 = Config().get(
                'motion_controller[*].servos[*].front_leg_right[*].pca9685 | [0] | [0] | [0]')
            servo_front_leg_right_channel = Config().get(
                'motion_controller[*].servos[*].front_leg_right[*].channel | [0] | [0] | [0]')
            servo_front_leg_right_min_pulse = Config().get(
                'motion_controller[*].servos[*].front_leg_right[*].min_pulse | [0] | [0] | [0]')
            servo_front_leg_right_max_pulse = Config().get(
                'motion_controller[*].servos[*].front_leg_right[*].max_pulse | [0] | [0] | [0]')

            if servo_front_leg_right_pca9685 == 1:
                self.servo_front_leg_right = servo.Servo(self.pca9685_1.channels[servo_front_leg_right_channel])
            else:
                self.servo_front_leg_right = servo.Servo(
                    self.pca9685_2.channels[servo_front_leg_right_channel])
            self.servo_front_leg_right.set_pulse_width_range(min_pulse=servo_front_leg_right_min_pulse,
                                                             max_pulse=servo_front_leg_right_max_pulse)

            servo_front_feet_right_pca9685 = Config().get(
                'motion_controller[*].servos[*].front_feet_right[*].pca9685 | [0] | [0] | [0]')
            servo_front_feet_right_channel = Config().get(
                'motion_controller[*].servos[*].front_feet_right[*].channel | [0] | [0] | [0]')
            servo_front_feet_right_min_pulse = Config().get(
                'motion_controller[*].servos[*].front_feet_right[*].min_pulse | [0] | [0] | [0]')
            servo_front_feet_right_max_pulse = Config().get(
                'motion_controller[*].servos[*].front_feet_right[*].max_pulse | [0] | [0] | [0]')

            if servo_front_feet_right_pca9685 == 1:
                self.servo_front_feet_right = servo.Servo(self.pca9685_1.channels[servo_front_feet_right_channel])
            else:
                self.servo_front_feet_right = servo.Servo(self.pca9685_2.channels[servo_front_feet_right_channel])
            self.servo_front_feet_right.set_pulse_width_range(min_pulse=servo_front_feet_right_min_pulse,
                                                              max_pulse=servo_front_feet_right_max_pulse)

            self.rest_position()

            self._abort_queue = communication_queues['abort_controller']
            self._motion_queue = communication_queues['motion_controller']
            self._lcd_screen_queue = communication_queues['lcd_screen_controller']

            if pca9685_2_address:
                self._lcd_screen_queue.put('motion_controller_1 OK')
                self._lcd_screen_queue.put('motion_controller_2 OK')
            else:
                self._lcd_screen_queue.put('motion_controller_1 OK')
                self._lcd_screen_queue.put('motion_controller_2 NOK')

            self._previous_event = {}

            log.info('Controller started')

        except Exception as e:
            log.error('No PCA9685 detected', e)
            self._lcd_screen_queue.put('motion_controller_1 NOK')
            self._lcd_screen_queue.put('motion_controller_2 NOK')
            sys.exit(1)

    def exit_gracefully(self, signum, frame):
        log.info('Terminated')
        sys.exit(0)

    def do_process_events_from_queues(self):

        try:

            while True:

                try:

                    # If we don't get an order in 60 seconds we disable the robot.
                    #event = self._motion_queue.get(block=True, timeout=30)
                    event = self._motion_queue.get()

                    log.debug(event)

                    event_diff = {}
                    if self._previous_event:
                        for key in event:
                            if event[key] != self._previous_event[key]:
                                event_diff[key] = event[key]

                    # screen is very low and un responsive, not good to print the buttons pushes
                    # log.debug(', '.join(event_diff))
                    # if not event_diff:
                    #    self._lcd_screen_queue.put('Line2 Inactive')
                    # else:
                    #    self._lcd_screen_queue.put('Line2 ' + str(event_diff)[1:-1].replace("'", ''))

                    # if event.startswith('activate'):
                    #    self.activate()

                    # if event.startswith('key press'):
                    #    self.move_to_position_xxx()

                    # if event.startswith('_Obstacle at 10cm'):
                    #    pass

                    if event['start']:
                        print('START')
                        self.activate()

                    if event['y']:
                        print('ABORT')
                        self.abort()

                    if event['a']:
                        print('You did press A, SpotMicro rest position')
                        self.rest_position()

                    if event['b']:
                        print('You did press B, SpotMicro Stop!')

                    if event['ly'] < 0 or event['hat0y'] < 0:
                        print('Moving forward ' + str(event['ly']))
                        self.move_forward()

                    if event['ly'] > 0 or event['hat0y'] > 0:
                        print('Moving backwards ' + str(event['ly']))
                        self.move_backwards()

                    if event['lx'] > 0 or event['hat0x'] > 0:
                        print('Spinning to the right ' + str(event['lx']))

                    if event['lx'] < 0 or event['hat0x'] < 0:
                        print('Spinning to the left ' + str(event['lx']))

                    self._previous_event = event

                except queue.Empty as e:
                    # This will happen after 30 seconds of inactivity
                    # If we don't get an order in 30 seconds we disable the robot.
                    log.info('Inactivity lasted 30 seconds, shutting down the servos, '
                             'press start to reactivate')
                    self.abort()

        except Exception as e:
            log.error('Unknown problem with the PCA9685 detected', e)

        finally:
            self.pca9685_1.deinit()
            if self.boards == 2:
                self.pca9685_2.deinit()

    def activate(self):
        self._abort_queue.put('activate_servos')

    def abort(self):
        self._abort_queue.put('abort')

    def rest_position(self):

        self.servo_rear_shoulder_left.angle = 0
        self.servo_rear_leg_left.angle = 75
        self.servo_rear_feet_left.angle = 30

        self.servo_rear_shoulder_right.angle = 102
        self.servo_rear_leg_right.angle = 120
        self.servo_rear_feet_right.angle = 160

        self.servo_front_shoulder_left.angle = 105
        self.servo_front_leg_left.angle = 65
        self.servo_front_feet_left.angle = 40

        self.servo_front_shoulder_right.angle = 105
        self.servo_front_leg_right.angle = 140
        self.servo_front_feet_right.angle = 165

    def move_to_position_xxx(self):
        pass

    def move_forward(self):
        log.debug("MOVING FORWARD!")
        self.servo_rear_shoulder_left.angle = 85 + 20
        self.servo_rear_leg_left.angle = 75 + 20
        self.servo_rear_feet_left.angle = 30 + 20

        self.servo_rear_shoulder_right.angle = 102 - 20
        self.servo_rear_leg_right.angle = 120 - 20
        self.servo_rear_feet_right.angle = 160 - 20

        self.servo_front_shoulder_left.angle = 105 + 20
        self.servo_front_leg_left.angle = 65 + 20
        self.servo_front_feet_left.angle = 40 + 20

        self.servo_front_shoulder_right.angle = 105 - 20
        self.servo_front_leg_right.angle = 140 - 20
        self.servo_front_feet_right.angle = 165 - 20

    def move_backwards(self):
        log.debug("MOVING BACKWARDS!")
        self.servo_rear_shoulder_left.angle = 85 + 20
        self.servo_rear_leg_left.angle = 75 + 20
        self.servo_rear_feet_left.angle = 30 + 20

        self.servo_rear_shoulder_right.angle = 102 - 20
        self.servo_rear_leg_right.angle = 120 - 20
        self.servo_rear_feet_right.angle = 160 - 20

        self.servo_front_shoulder_left.angle = 105 + 20
        self.servo_front_leg_left.angle = 65 + 20
        self.servo_front_feet_left.angle = 40 + 20

        self.servo_front_shoulder_right.angle = 105 - 20
        self.servo_front_leg_right.angle = 140 - 20
        self.servo_front_feet_right.angle = 165 - 20
