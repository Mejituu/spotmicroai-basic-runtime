import time

from spotmicroai.utilities.log import Logger
from spotmicroai.utilities.config import Config
from spotmicroai.utilities.general import General

log = Logger().setup_logger('Motion controller leg moves')


class MotionController:

    def __init__(self):
        pass

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

        self.servo_arm_rotation.angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_ROTATION_REST_ANGLE)
        self.servo_arm_lift.angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_LIFT_REST_ANGLE)
        self.servo_arm_range.angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_RANGE_REST_ANGLE)
        self.servo_arm_cam_tilt.angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_CAM_TILT_REST_ANGLE)

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

    def standing_position(self):

        variation_leg = 50
        variation_feet = 70

        self.servo_rear_shoulder_left.angle = self.servo_rear_shoulder_left_rest_angle + 10
        self.servo_rear_leg_left.angle = self.servo_rear_leg_left_rest_angle - variation_leg
        self.servo_rear_feet_left.angle = self.servo_rear_feet_left_rest_angle + variation_feet

        self.servo_rear_shoulder_right.angle = self.servo_rear_shoulder_right_rest_angle - 10
        self.servo_rear_leg_right.angle = self.servo_rear_leg_right_rest_angle + variation_leg
        self.servo_rear_feet_right.angle = self.servo_rear_feet_right_rest_angle - variation_feet

        time.sleep(0.05)

        self.servo_front_shoulder_left.angle = self.servo_front_shoulder_left_rest_angle - 10
        self.servo_front_leg_left.angle = self.servo_front_leg_left_rest_angle - variation_leg + 5
        self.servo_front_feet_left.angle = self.servo_front_feet_left_rest_angle + variation_feet - 5

        self.servo_front_shoulder_right.angle = self.servo_front_shoulder_right_rest_angle + 10
        self.servo_front_leg_right.angle = self.servo_front_leg_right_rest_angle + variation_leg - 5
        self.servo_front_feet_right.angle = self.servo_front_feet_right_rest_angle - variation_feet + 5

    def body_move_position_right(self):

        move = 20

        variation_leg = 50
        variation_feet = 70

        self.servo_rear_shoulder_left.angle = self.servo_rear_shoulder_left_rest_angle + 10 + move
        self.servo_rear_leg_left.angle = self.servo_rear_leg_left_rest_angle - variation_leg
        self.servo_rear_feet_left.angle = self.servo_rear_feet_left_rest_angle + variation_feet

        self.servo_rear_shoulder_right.angle = self.servo_rear_shoulder_right_rest_angle - 10 + move
        self.servo_rear_leg_right.angle = self.servo_rear_leg_right_rest_angle + variation_leg
        self.servo_rear_feet_right.angle = self.servo_rear_feet_right_rest_angle - variation_feet

        time.sleep(0.05)

        self.servo_front_shoulder_left.angle = self.servo_front_shoulder_left_rest_angle - 10 - move
        self.servo_front_leg_left.angle = self.servo_front_leg_left_rest_angle - variation_leg + 5
        self.servo_front_feet_left.angle = self.servo_front_feet_left_rest_angle + variation_feet - 5

        self.servo_front_shoulder_right.angle = self.servo_front_shoulder_right_rest_angle + 10 - move
        self.servo_front_leg_right.angle = self.servo_front_leg_right_rest_angle + variation_leg - 5
        self.servo_front_feet_right.angle = self.servo_front_feet_right_rest_angle - variation_feet + 5

    def body_move_position_left(self):

        move = 20

        variation_leg = 50
        variation_feet = 70

        self.servo_rear_shoulder_left.angle = self.servo_rear_shoulder_left_rest_angle + 10 - move
        self.servo_rear_leg_left.angle = self.servo_rear_leg_left_rest_angle - variation_leg
        self.servo_rear_feet_left.angle = self.servo_rear_feet_left_rest_angle + variation_feet

        self.servo_rear_shoulder_right.angle = self.servo_rear_shoulder_right_rest_angle - 10 - move
        self.servo_rear_leg_right.angle = self.servo_rear_leg_right_rest_angle + variation_leg
        self.servo_rear_feet_right.angle = self.servo_rear_feet_right_rest_angle - variation_feet

        time.sleep(0.05)

        self.servo_front_shoulder_left.angle = self.servo_front_shoulder_left_rest_angle - 10 + move
        self.servo_front_leg_left.angle = self.servo_front_leg_left_rest_angle - variation_leg + 5
        self.servo_front_feet_left.angle = self.servo_front_feet_left_rest_angle + variation_feet - 5

        self.servo_front_shoulder_right.angle = self.servo_front_shoulder_right_rest_angle + 10 + move
        self.servo_front_leg_right.angle = self.servo_front_leg_right_rest_angle + variation_leg - 5
        self.servo_front_feet_right.angle = self.servo_front_feet_right_rest_angle - variation_feet + 5
