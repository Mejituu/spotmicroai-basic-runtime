import time

from spotmicroai.utilities.log import Logger
from spotmicroai.utilities.config import Config
from spotmicroai.utilities.general import General

from spotmicroai.motion_controller.motion_controller_setup import MotionControllerSetup

log = Logger().setup_logger('Motion controller legs moves')


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MotionControllerLegsMoves(metaclass=Singleton):
    servo_rear_shoulder_left_angle = None
    servo_rear_leg_left_angle = None
    servo_rear_feet_left_angle = None
    servo_rear_shoulder_right_angle = None
    servo_rear_leg_right_angle = None
    servo_rear_feet_right_angle = None
    servo_front_shoulder_left_angle = None
    servo_front_leg_left_angle = None
    servo_front_feet_left_angle = None
    servo_front_shoulder_right_angle = None
    servo_front_leg_right_angle = None
    servo_front_feet_right_angle = None

    def __init__(self):
        pass

    def move(self):

        if not MotionControllerSetup().legs_are_enabled:
            return

        try:
            MotionControllerSetup().servo_rear_shoulder_left.angle = self.servo_rear_shoulder_left_angle
        except ValueError as e:
            log.error('Impossible servo_rear_shoulder_left angle requested: ' + str(self.servo_rear_shoulder_left_angle))

        try:
            MotionControllerSetup().servo_rear_leg_left.angle = self.servo_rear_leg_left_angle
        except ValueError as e:
            log.error('Impossible servo_rear_leg_left angle requested: ' + str(self.servo_rear_leg_left_angle))

        try:
            MotionControllerSetup().servo_rear_feet_left.angle = self.servo_rear_feet_left_angle
        except ValueError as e:
            log.error('Impossible servo_rear_feet_left angle requested: ' + str(self.servo_rear_feet_left_angle))

        try:
            MotionControllerSetup().servo_rear_shoulder_right.angle = self.servo_rear_shoulder_right_angle
        except ValueError as e:
            log.error('Impossible servo_rear_shoulder_right angle requested: ' + str(self.servo_rear_shoulder_right_angle))

        try:
            MotionControllerSetup().servo_rear_leg_right.angle = self.servo_rear_leg_right_angle
        except ValueError as e:
            log.error('Impossible servo_rear_leg_right angle requested: ' + str(self.servo_rear_leg_right_angle))

        try:
            MotionControllerSetup().servo_rear_feet_right.angle = self.servo_rear_feet_right_angle
        except ValueError as e:
            log.error('Impossible servo_rear_feet_right angle requested: ' + str(self.servo_rear_feet_right_angle))

        try:
            MotionControllerSetup().servo_front_shoulder_left.angle = self.servo_front_shoulder_left_angle
        except ValueError as e:
            log.error('Impossible servo_front_shoulder_left angle requested: ' + str(self.servo_front_shoulder_left_angle))

        try:
            MotionControllerSetup().servo_front_leg_left.angle = self.servo_front_leg_left_angle
        except ValueError as e:
            log.error('Impossible servo_front_leg_left angle requested: ' + str(self.servo_front_leg_left_angle))

        try:
            MotionControllerSetup().servo_front_feet_left.angle = self.servo_front_feet_left_angle
        except ValueError as e:
            log.error('Impossible servo_front_feet_left angle requested: ' + str(self.servo_front_feet_left_angle))

        try:
            MotionControllerSetup().servo_front_shoulder_right.angle = self.servo_front_shoulder_right_angle
        except ValueError as e:
            log.error('Impossible servo_front_shoulder_right angle requested: ' + str(self.servo_front_shoulder_right_angle))

        try:
            MotionControllerSetup().servo_front_leg_right.angle = self.servo_front_leg_right_angle
        except ValueError as e:
            log.error('Impossible servo_front_leg_right angle requested: ' + str(self.servo_front_leg_right_angle))

        try:
            MotionControllerSetup().servo_front_feet_right.angle = self.servo_front_feet_right_angle
        except ValueError as e:
            log.error('Impossible servo_front_feet_right angle requested: ' + str(self.servo_front_feet_right_angle))

    def rest_position(self):

        MotionControllerSetup().servo_rear_shoulder_left_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_LEFT_REST_ANGLE)
        MotionControllerSetup().servo_rear_leg_left_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_LEFT_REST_ANGLE)
        MotionControllerSetup().servo_rear_feet_left_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_LEFT_REST_ANGLE)
        MotionControllerSetup().servo_rear_shoulder_right_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_RIGHT_REST_ANGLE)
        MotionControllerSetup().servo_rear_leg_right_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_RIGHT_REST_ANGLE)
        MotionControllerSetup().servo_rear_feet_right_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_RIGHT_REST_ANGLE)
        MotionControllerSetup().servo_front_shoulder_left_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_LEFT_REST_ANGLE)
        MotionControllerSetup().servo_front_leg_left_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_LEFT_REST_ANGLE)
        MotionControllerSetup().servo_front_feet_left_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_LEFT_REST_ANGLE)
        MotionControllerSetup().servo_front_shoulder_right_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_RIGHT_REST_ANGLE)
        MotionControllerSetup().servo_front_leg_right_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_RIGHT_REST_ANGLE)
        MotionControllerSetup().servo_front_feet_right_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_RIGHT_REST_ANGLE)

    def body_move_body_up_and_down(self, raw_value):

        range = 10
        range2 = 15

        if raw_value < 0:
            self.servo_rear_leg_left_angle -= range
            self.servo_rear_feet_left_angle += range2
            self.servo_rear_leg_right_angle += range
            self.servo_rear_feet_right_angle -= range2
            self.servo_front_leg_left_angle -= range
            self.servo_front_feet_left_angle += range2
            self.servo_front_leg_right_angle += range
            self.servo_front_feet_right_angle -= range2

        elif raw_value > 0:
            self.servo_rear_leg_left_angle += range
            self.servo_rear_feet_left_angle -= range2
            self.servo_rear_leg_right_angle -= range
            self.servo_rear_feet_right_angle += range2
            self.servo_front_leg_left_angle += range
            self.servo_front_feet_left_angle -= range2
            self.servo_front_leg_right_angle -= range
            self.servo_front_feet_right_angle += range2

        else:
            self.rest_position()

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

        self.servo_rear_leg_left_angle = delta_rear_leg_left
        self.servo_rear_feet_left_angle = delta_rear_feet_left
        self.servo_rear_leg_right_angle = delta_rear_leg_right
        self.servo_rear_feet_right_angle = delta_rear_feet_right
        self.servo_front_leg_left_angle = delta_front_leg_left
        self.servo_front_feet_left_angle = delta_front_feet_left
        self.servo_front_leg_right_angle = delta_front_leg_right
        self.servo_front_feet_right_angle = delta_front_feet_right

    def body_move_body_left_right(self, raw_value):

        range = 5

        if raw_value < 0:
            self.servo_rear_shoulder_left_angle -= range
            self.servo_rear_shoulder_right_angle -= range
            self.servo_front_shoulder_left_angle += range
            self.servo_front_shoulder_right_angle += range

        elif raw_value > 0:
            self.servo_rear_shoulder_left_angle += range
            self.servo_rear_shoulder_right_angle += range
            self.servo_front_shoulder_left_angle -= range
            self.servo_front_shoulder_right_angle -= range

        else:
            self.rest_position()

    def body_move_body_left_right_analog(self, raw_value):

        delta_a = int(General().maprange((-1, 1), (30, 150), raw_value))
        delta_b = int(General().maprange((-1, 1), (150, 30), raw_value))

        self.servo_rear_shoulder_left_angle = delta_a
        self.servo_rear_shoulder_right_angle = delta_a
        self.servo_front_shoulder_left_angle = delta_b
        self.servo_front_shoulder_right_angle = delta_b

    def standing_position(self):

        variation_leg = 50
        variation_feet = 70

        MotionControllerSetup().servo_rear_shoulder_left.angle = self.servo_rear_shoulder_left_angle + 10
        MotionControllerSetup().servo_rear_leg_left.angle = self.servo_rear_leg_left_angle - variation_leg
        MotionControllerSetup().servo_rear_feet_left.angle = self.servo_rear_feet_left_angle + variation_feet

        MotionControllerSetup().servo_rear_shoulder_right.angle = self.servo_rear_shoulder_right_angle - 10
        MotionControllerSetup().servo_rear_leg_right.angle = self.servo_rear_leg_right_angle + variation_leg
        MotionControllerSetup().servo_rear_feet_right.angle = self.servo_rear_feet_right_angle - variation_feet

        time.sleep(0.05)

        MotionControllerSetup().servo_front_shoulder_left.angle = self.servo_front_shoulder_left_angle - 10
        MotionControllerSetup().servo_front_leg_left.angle = self.servo_front_leg_left_angle - variation_leg + 5
        MotionControllerSetup().servo_front_feet_left.angle = self.servo_front_feet_left_angle + variation_feet - 5

        MotionControllerSetup().servo_front_shoulder_right.angle = self.servo_front_shoulder_right_angle + 10
        MotionControllerSetup().servo_front_leg_right.angle = self.servo_front_leg_right_angle + variation_leg - 5
        MotionControllerSetup().servo_front_feet_right.angle = self.servo_front_feet_right_angle - variation_feet + 5

    def body_move_position_right(self):

        move = 20

        variation_leg = 50
        variation_feet = 70

        MotionControllerSetup().servo_rear_shoulder_left.angle = self.servo_rear_shoulder_left_angle + 10 + move
        MotionControllerSetup().servo_rear_leg_left.angle = self.servo_rear_leg_left_angle - variation_leg
        MotionControllerSetup().servo_rear_feet_left.angle = self.servo_rear_feet_left_angle + variation_feet

        MotionControllerSetup().servo_rear_shoulder_right.angle = self.servo_rear_shoulder_right_angle - 10 + move
        MotionControllerSetup().servo_rear_leg_right.angle = self.servo_rear_leg_right_angle + variation_leg
        MotionControllerSetup().servo_rear_feet_right.angle = self.servo_rear_feet_right_angle - variation_feet

        time.sleep(0.05)

        MotionControllerSetup().servo_front_shoulder_left.angle = self.servo_front_shoulder_left_angle - 10 - move
        MotionControllerSetup().servo_front_leg_left.angle = self.servo_front_leg_left_angle - variation_leg + 5
        MotionControllerSetup().servo_front_feet_left.angle = self.servo_front_feet_left_angle + variation_feet - 5

        MotionControllerSetup().servo_front_shoulder_right.angle = self.servo_front_shoulder_right_angle + 10 - move
        MotionControllerSetup().servo_front_leg_right.angle = self.servo_front_leg_right_angle + variation_leg - 5
        MotionControllerSetup().servo_front_feet_right.angle = self.servo_front_feet_right_angle - variation_feet + 5

    def body_move_position_left(self):

        move = 20

        variation_leg = 50
        variation_feet = 70

        MotionControllerSetup().servo_rear_shoulder_left.angle = self.servo_rear_shoulder_left_angle + 10 - move
        MotionControllerSetup().servo_rear_leg_left.angle = self.servo_rear_leg_left_angle - variation_leg
        MotionControllerSetup().servo_rear_feet_left.angle = self.servo_rear_feet_left_angle + variation_feet

        MotionControllerSetup().servo_rear_shoulder_right.angle = self.servo_rear_shoulder_right_angle - 10 - move
        MotionControllerSetup().servo_rear_leg_right.angle = self.servo_rear_leg_right_angle + variation_leg
        MotionControllerSetup().servo_rear_feet_right.angle = self.servo_rear_feet_right_angle - variation_feet

        time.sleep(0.05)

        MotionControllerSetup().servo_front_shoulder_left.angle = self.servo_front_shoulder_left_angle - 10 + move
        MotionControllerSetup().servo_front_leg_left.angle = self.servo_front_leg_left_angle - variation_leg + 5
        MotionControllerSetup().servo_front_feet_left.angle = self.servo_front_feet_left_angle + variation_feet - 5

        MotionControllerSetup().servo_front_shoulder_right.angle = self.servo_front_shoulder_right_angle + 10 + move
        MotionControllerSetup().servo_front_leg_right.angle = self.servo_front_leg_right_angle + variation_leg - 5
        MotionControllerSetup().servo_front_feet_right.angle = self.servo_front_feet_right_angle - variation_feet + 5
