from spotmicroai.utilities.log import Logger
from spotmicroai.utilities.config import Config
from spotmicroai.utilities.general import General

from spotmicroai.motion_controller.motion_controller_setup import MotionControllerSetup

log = Logger().setup_logger('Motion controller arm moves')


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MotionControllerArmMoves(metaclass=Singleton):
    servo_arm_rotation_angle = None
    servo_arm_lift_angle = None
    servo_arm_range_angle = None
    servo_arm_cam_tilt_angle = None

    def __init__(self):
        pass

    def move(self):

        if not MotionControllerSetup().arm_is_enabled:
            return

        try:
            MotionControllerSetup().servo_arm_rotation.angle = self.servo_arm_rotation_angle
        except ValueError as e:
            log.error('Impossible servo_arm_rotation angle requested' + str(self.servo_arm_rotation_angle))

        try:
            MotionControllerSetup().servo_arm_lift.angle = self.servo_arm_lift_angle
        except ValueError as e:
            log.error('Impossible arm_lift angle requested' + str(self.servo_arm_lift_angle))

        try:
            MotionControllerSetup().servo_arm_range.angle = self.servo_arm_range_angle
        except ValueError as e:
            log.error('Impossible servo_arm_range angle requested' + str(self.servo_arm_range_angle))

        try:
            MotionControllerSetup().servo_arm_cam_tilt.angle = self.servo_arm_cam_tilt_angle
        except ValueError as e:
            log.error('Impossible servo_arm_cam_tilt angle requested' + str(self.servo_arm_cam_tilt_angle))

    def rest_position(self):

        if not MotionControllerSetup().arm_is_enabled:
            return

        MotionControllerSetup().servo_arm_rotation.angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_ROTATION_REST_ANGLE)
        MotionControllerSetup().servo_arm_lift.angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_LIFT_REST_ANGLE)
        MotionControllerSetup().servo_arm_range.angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_RANGE_REST_ANGLE)
        MotionControllerSetup().servo_arm_cam_tilt.angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_CAM_TILT_REST_ANGLE)

    def arm_set_rotation(self, raw_value):

        if not MotionControllerSetup().arm_is_enabled:
            return

        left_position = int(General().maprange((-1, 1), (0, 180), raw_value / 2))

        if int(MotionControllerSetup().servo_arm_rotation.angle) != int(left_position):
            MotionControllerSetup().servo_arm_rotation.angle = left_position

    def arm_set_lift(self, raw_value):

        if not MotionControllerSetup().arm_is_enabled:
            return

        lift_position = int(General().maprange((-1, 1), (180, 0), raw_value / 2))

        if int(MotionControllerSetup().servo_arm_lift.angle) != int(lift_position):
            MotionControllerSetup().servo_arm_lift.angle = lift_position

    def arm_set_range(self, raw_value):

        if not MotionControllerSetup().arm_is_enabled:
            return

        range_position = int(General().maprange((-1, 1), (180, 0), raw_value / 2))

        if int(MotionControllerSetup().servo_arm_range.angle) != int(range_position):
            MotionControllerSetup().servo_arm_range.angle = range_position

    def arm_set_cam_tilt(self, raw_value):

        if not MotionControllerSetup().arm_is_enabled:
            return

        tilt_position = int(General().maprange((-1, 1), (100, 150), raw_value))

        if int(MotionControllerSetup().servo_arm_cam_tilt.angle) != int(tilt_position):
            MotionControllerSetup().servo_arm_cam_tilt.angel = tilt_position
