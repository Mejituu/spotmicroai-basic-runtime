
from spotmicroai.utilities.log import Logger
from spotmicroai.utilities.config import Config
from spotmicroai.utilities.general import General

log = Logger().setup_logger('Motion controller arm moves')


class MotionController:

    def __init__(self, communication_queues):
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

        try:
            self.servo_arm_rotation.angle = self.servo_arm_rotation_rest_angle
        except ValueError as e:
            log.error('Impossible servo_arm_rotation angle requested')

        try:
            self.servo_arm_lift.angle = self.servo_arm_lift_rest_angle
        except ValueError as e:
            log.error('Impossible arm_lift angle requested')

        try:
            self.servo_arm_range.angle = self.servo_arm_range_rest_angle
        except ValueError as e:
            log.error('Impossible servo_arm_range angle requested')

        try:
            self.servo_arm_cam_tilt.angle = self.servo_arm_cam_tilt_rest_angle
        except ValueError as e:
            log.error('Impossible servo_arm_cam_tilt angle requested')

    def rest_position(self):

        self.servo_arm_rotation.angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_ROTATION_REST_ANGLE)
        self.servo_arm_lift.angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_LIFT_REST_ANGLE)
        self.servo_arm_range.angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_RANGE_REST_ANGLE)
        self.servo_arm_cam_tilt.angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_CAM_TILT_REST_ANGLE)

    def arm_set_rotation(self, raw_value):

        left_position = int(General().maprange((-1, 1), (0, 180), raw_value / 2))

        if int(self.servo_arm_rotation.angle) != int(left_position):
            self.servo_arm_rotation.angle = left_position

    def arm_set_lift(self, raw_value):

        lift_position = int(General().maprange((-1, 1), (180, 0), raw_value / 2))

        if int(self.servo_arm_lift.angle) != int(lift_position):
            self.servo_arm_lift.angle = lift_position

    def arm_set_range(self, raw_value):

        range_position = int(General().maprange((-1, 1), (180, 0), raw_value / 2))

        if int(self.servo_arm_range.angle) != int(range_position):
            self.servo_arm_range.angle = range_position

    def arm_set_cam_tilt(self, raw_value):

        tilt_position = int(General().maprange((-1, 1), (100, 150), raw_value))

        if int(self.servo_arm_cam_tilt.angle) != int(tilt_position):
            self.servo_arm_cam_tilt.angel = tilt_position
