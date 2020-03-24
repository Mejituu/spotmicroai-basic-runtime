import signal
import sys

import queue
import busio
from board import SCL, SDA
import time

from spotmicroai.utilities.log import Logger
import spotmicroai.utilities.queues as queues

from spotmicroai.motion_controller.motion_controller_setup import MotionControllerSetup
from spotmicroai.motion_controller.arm_moves import MotionControllerArmMoves
from spotmicroai.motion_controller.legs_moves import MotionControllerLegsMoves

log = Logger().setup_logger('Motion controller')


class MotionController:
    boards = 1

    is_activated = False

    def __init__(self, communication_queues):

        try:

            log.debug('Starting controller...')

            signal.signal(signal.SIGINT, self.exit_gracefully)
            signal.signal(signal.SIGTERM, self.exit_gracefully)

            self.i2c = busio.I2C(SCL, SDA)

            self._abort_queue = communication_queues[queues.ABORT_CONTROLLER]
            self._motion_queue = communication_queues[queues.MOTION_CONTROLLER]
            self._lcd_screen_queue = communication_queues[queues.LCD_SCREEN_CONTROLLER]

            if MotionControllerSetup().pca9685_1:
                self._lcd_screen_queue.put('motion_controller_1 OK')
            else:
                self._lcd_screen_queue.put('motion_controller_1 NOK')

            if MotionControllerSetup().pca9685_2:
                self._lcd_screen_queue.put('motion_controller_2 OK')
            else:
                self._lcd_screen_queue.put('motion_controller_2 NOK')

            self._previous_event = {}

        except Exception as e:
            log.error('Motion controller initialization problem', e)
            self._lcd_screen_queue.put('motion_controller_1 NOK')
            self._lcd_screen_queue.put('motion_controller_2 NOK')
            try:
                MotionControllerSetup().deactivate_pca9685_boards()
            finally:
                sys.exit(1)

    def exit_gracefully(self, signum, frame):
        try:
            MotionControllerSetup().deactivate_pca9685_boards()
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
                        MotionControllerLegsMoves().rest_position()
                        MotionControllerArmMoves().rest_position()
                        time.sleep(0.5)
                        MotionControllerSetup().deactivate_pca9685_boards()
                        self._abort_queue.put(queues.ABORT_CONTROLLER_ACTION_ABORT)
                    else:
                        self._abort_queue.put(queues.ABORT_CONTROLLER_ACTION_ACTIVATE)
                        MotionControllerSetup().activate_pca9685_boards()
                        self.is_activated = True
                        MotionControllerSetup().activate_servos()
                        MotionControllerLegsMoves().rest_position()
                        MotionControllerArmMoves().rest_position()

                if not self.is_activated:
                    log.info('Press START/OPTIONS to enable the servos')
                    continue

                if event['a']:
                    MotionControllerLegsMoves().rest_position()
                    MotionControllerArmMoves().rest_position()

                if event['hat0y']:
                    MotionControllerLegsMoves().body_move_body_up_and_down(event['hat0y'])

                if event['hat0x']:
                    MotionControllerLegsMoves().body_move_body_left_right(event['hat0x'])

                if event['ry']:
                    MotionControllerLegsMoves().body_move_body_up_and_down_analog(event['ry'])

                if event['rx']:
                    MotionControllerLegsMoves().body_move_body_left_right_analog(event['rx'])

                if event['hat0x'] and event['tl2']:
                    # 2 buttons example
                    pass

                if event['y']:
                    MotionControllerLegsMoves().standing_position()

                if event['b']:
                    MotionControllerLegsMoves().body_move_position_right()

                if event['x']:
                    MotionControllerLegsMoves().body_move_position_left()

                if event['tl']:
                    MotionControllerArmMoves().arm_set_rotation(event['lx'])

                if event['tl']:
                    MotionControllerArmMoves().arm_set_lift(event['ly'])

                if event['tr']:
                    MotionControllerArmMoves().arm_set_range(event['ly'])

                if event['tr']:
                    MotionControllerArmMoves().arm_set_cam_tilt(event['ry'])

                MotionControllerLegsMoves().move()
                MotionControllerArmMoves().move()

            except queue.Empty as e:
                log.info('Inactivity lasted 60 seconds, shutting down the servos, '
                         'press START/OPTIONS button to reactivate')
                if self.is_activated:
                    MotionControllerLegsMoves().rest_position()
                    MotionControllerArmMoves().rest_position()
                    time.sleep(0.5)
                    MotionControllerSetup().deactivate_pca9685_boards()
                    self.is_activated = False

            except Exception as e:
                log.error('Unknown problem while processing the queue of the motion controller')
                log.error(' - Most likely a servo is not able to get to the assigned position', e)
