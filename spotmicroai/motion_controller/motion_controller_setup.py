from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

from spotmicroai.utilities.log import Logger
from spotmicroai.utilities.config import Config

log = Logger().setup_logger('Motion controller setup')


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class MotionControllerSetup(metaclass=Singleton):
    i2c = None

    pca9685_1 = None
    pca9685_2 = None

    legs_are_enabled = None

    servo_rear_shoulder_left = None
    servo_rear_leg_left = None
    servo_rear_feet_left = None
    servo_rear_shoulder_right = None
    servo_rear_leg_right = None
    servo_rear_feet_right = None
    servo_front_shoulder_left = None
    servo_front_leg_left = None
    servo_front_feet_left = None
    servo_front_shoulder_right = None
    servo_front_leg_right = None
    servo_front_feet_right = None

    arm_is_enabled = None

    servo_arm_rotation = None
    servo_arm_lift = None
    servo_arm_range = None
    servo_arm_cam_tilt = None

    def __init__(self):
        self.legs_are_enabled = Config().get(Config.MOTION_CONTROLLER_LEGS_ARE_ENABLED)
        self.arm_is_enabled = Config().get(Config.MOTION_CONTROLLER_ARM_IS_ENABLED)

    def activate_pca9685_boards(self):

        log.debug('Activating PCA9685 board(s)...')

        try:
            pca9685_1_enabled = int(Config().get(Config.MOTION_CONTROLLER_BOARDS_PCA9685_1_ENABLED), 0)
            pca9685_1_address = int(Config().get(Config.MOTION_CONTROLLER_BOARDS_PCA9685_1_ADDRESS), 0)
            pca9685_1_reference_clock_speed = int(Config().get(Config.MOTION_CONTROLLER_BOARDS_PCA9685_1_REFERENCE_CLOCK_SPEED))
            pca9685_1_frequency = int(Config().get(Config.MOTION_CONTROLLER_BOARDS_PCA9685_1_FREQUENCY))

            if pca9685_1_enabled:
                self.pca9685_1 = PCA9685(self.i2c,
                                         address=pca9685_1_address,
                                         reference_clock_speed=pca9685_1_reference_clock_speed)
                self.pca9685_1.frequency = pca9685_1_frequency

        except Exception as e:
            self.pca9685_1 = None
            log.debug("PCA9685 1 is not present")

        try:
            pca9685_2_enabled = int(Config().get(Config.MOTION_CONTROLLER_BOARDS_PCA9685_2_ENABLED), 0)
            pca9685_2_address = int(Config().get(Config.MOTION_CONTROLLER_BOARDS_PCA9685_2_ADDRESS), 0)
            pca9685_2_reference_clock_speed = int(Config().get(Config.MOTION_CONTROLLER_BOARDS_PCA9685_2_REFERENCE_CLOCK_SPEED))
            pca9685_2_frequency = int(Config().get(Config.MOTION_CONTROLLER_BOARDS_PCA9685_2_FREQUENCY))

            if pca9685_2_enabled:
                self.pca9685_2 = PCA9685(self.i2c,
                                         address=pca9685_2_address,
                                         reference_clock_speed=pca9685_2_reference_clock_speed)
                self.pca9685_2.frequency = pca9685_2_frequency

        except Exception as e:
            self.pca9685_2 = None
            log.debug("PCA9685 2 is not present")

    def deactivate_pca9685_boards(self):

        try:
            if self.pca9685_1:
                self.pca9685_1.deinit()
        finally:
            try:
                if self.pca9685_2:
                    self.pca9685_2.deinit()
            finally:
                pass

        log.debug('PCA9685 board(s) deactivated')

    def activate_servos(self):

        if self.legs_are_enabled:

            servo_rear_shoulder_left_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_LEFT_PCA9685)
            servo_rear_shoulder_left_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_LEFT_CHANNEL)
            servo_rear_shoulder_left_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_LEFT_MIN_PULSE)
            servo_rear_shoulder_left_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_LEFT_MAX_PULSE)

            if servo_rear_shoulder_left_pca9685 == 1:
                self.servo_rear_shoulder_left = servo.Servo(self.pca9685_1.channels[servo_rear_shoulder_left_channel])
            else:
                self.servo_rear_shoulder_left = servo.Servo(self.pca9685_2.channels[servo_rear_shoulder_left_channel])
            self.servo_rear_shoulder_left.set_pulse_width_range(min_pulse=servo_rear_shoulder_left_min_pulse,
                                                                max_pulse=servo_rear_shoulder_left_max_pulse)

            servo_rear_leg_left_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_LEFT_PCA9685)
            servo_rear_leg_left_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_LEFT_CHANNEL)
            servo_rear_leg_left_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_LEFT_MIN_PULSE)
            servo_rear_leg_left_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_LEFT_MAX_PULSE)

            if servo_rear_leg_left_pca9685 == 1:
                self.servo_rear_leg_left = servo.Servo(self.pca9685_1.channels[servo_rear_leg_left_channel])
            else:
                self.servo_rear_leg_left = servo.Servo(self.pca9685_2.channels[servo_rear_leg_left_channel])
            self.servo_rear_leg_left.set_pulse_width_range(min_pulse=servo_rear_leg_left_min_pulse, max_pulse=servo_rear_leg_left_max_pulse)

            servo_rear_feet_left_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_LEFT_PCA9685)
            servo_rear_feet_left_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_LEFT_CHANNEL)
            servo_rear_feet_left_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_LEFT_MIN_PULSE)
            servo_rear_feet_left_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_LEFT_MAX_PULSE)

            if servo_rear_feet_left_pca9685 == 1:
                self.servo_rear_feet_left = servo.Servo(self.pca9685_1.channels[servo_rear_feet_left_channel])
            else:
                self.servo_rear_feet_left = servo.Servo(self.pca9685_2.channels[servo_rear_feet_left_channel])
            self.servo_rear_feet_left.set_pulse_width_range(min_pulse=servo_rear_feet_left_min_pulse, max_pulse=servo_rear_feet_left_max_pulse)

            servo_rear_shoulder_right_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_RIGHT_PCA9685)
            servo_rear_shoulder_right_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_RIGHT_CHANNEL)
            servo_rear_shoulder_right_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_RIGHT_MIN_PULSE)
            servo_rear_shoulder_right_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_SHOULDER_RIGHT_MAX_PULSE)

            if servo_rear_shoulder_right_pca9685 == 1:
                self.servo_rear_shoulder_right = servo.Servo(self.pca9685_1.channels[servo_rear_shoulder_right_channel])
            else:
                self.servo_rear_shoulder_right = servo.Servo(self.pca9685_2.channels[servo_rear_shoulder_right_channel])
            self.servo_rear_shoulder_right.set_pulse_width_range(min_pulse=servo_rear_shoulder_right_min_pulse, max_pulse=servo_rear_shoulder_right_max_pulse)

            servo_rear_leg_right_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_RIGHT_PCA9685)
            servo_rear_leg_right_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_RIGHT_CHANNEL)
            servo_rear_leg_right_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_RIGHT_MIN_PULSE)
            servo_rear_leg_right_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_LEG_RIGHT_MAX_PULSE)

            if servo_rear_leg_right_pca9685 == 1:
                self.servo_rear_leg_right = servo.Servo(self.pca9685_1.channels[servo_rear_leg_right_channel])
            else:
                self.servo_rear_leg_right = servo.Servo(self.pca9685_2.channels[servo_rear_leg_right_channel])
            self.servo_rear_leg_right.set_pulse_width_range(min_pulse=servo_rear_leg_right_min_pulse, max_pulse=servo_rear_leg_right_max_pulse)

            servo_rear_feet_right_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_RIGHT_PCA9685)
            servo_rear_feet_right_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_RIGHT_CHANNEL)
            servo_rear_feet_right_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_RIGHT_MIN_PULSE)
            servo_rear_feet_right_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_REAR_FEET_RIGHT_MAX_PULSE)

            if servo_rear_feet_right_pca9685 == 1:
                self.servo_rear_feet_right = servo.Servo(self.pca9685_1.channels[servo_rear_feet_right_channel])
            else:
                self.servo_rear_feet_right = servo.Servo(self.pca9685_2.channels[servo_rear_feet_right_channel])
            self.servo_rear_feet_right.set_pulse_width_range(min_pulse=servo_rear_feet_right_min_pulse, max_pulse=servo_rear_feet_right_max_pulse)

            servo_front_shoulder_left_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_LEFT_PCA9685)
            servo_front_shoulder_left_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_LEFT_CHANNEL)
            servo_front_shoulder_left_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_LEFT_MIN_PULSE)
            servo_front_shoulder_left_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_LEFT_MAX_PULSE)

            if servo_front_shoulder_left_pca9685 == 1:
                self.servo_front_shoulder_left = servo.Servo(self.pca9685_1.channels[servo_front_shoulder_left_channel])
            else:
                self.servo_front_shoulder_left = servo.Servo(self.pca9685_2.channels[servo_front_shoulder_left_channel])
            self.servo_front_shoulder_left.set_pulse_width_range(min_pulse=servo_front_shoulder_left_min_pulse, max_pulse=servo_front_shoulder_left_max_pulse)

            servo_front_leg_left_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_LEFT_PCA9685)
            servo_front_leg_left_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_LEFT_CHANNEL)
            servo_front_leg_left_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_LEFT_MIN_PULSE)
            servo_front_leg_left_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_LEFT_MAX_PULSE)

            if servo_front_leg_left_pca9685 == 1:
                self.servo_front_leg_left = servo.Servo(self.pca9685_1.channels[servo_front_leg_left_channel])
            else:
                self.servo_front_leg_left = servo.Servo(self.pca9685_2.channels[servo_front_leg_left_channel])
            self.servo_front_leg_left.set_pulse_width_range(min_pulse=servo_front_leg_left_min_pulse, max_pulse=servo_front_leg_left_max_pulse)

            servo_front_feet_left_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_LEFT_PCA9685)
            servo_front_feet_left_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_LEFT_CHANNEL)
            servo_front_feet_left_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_LEFT_MIN_PULSE)
            servo_front_feet_left_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_LEFT_MAX_PULSE)

            if servo_front_feet_left_pca9685 == 1:
                self.servo_front_feet_left = servo.Servo(self.pca9685_1.channels[servo_front_feet_left_channel])
            else:
                self.servo_front_feet_left = servo.Servo(self.pca9685_2.channels[servo_front_feet_left_channel])
            self.servo_front_feet_left.set_pulse_width_range(min_pulse=servo_front_feet_left_min_pulse, max_pulse=servo_front_feet_left_max_pulse)

            servo_front_shoulder_right_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_RIGHT_PCA9685)
            servo_front_shoulder_right_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_RIGHT_CHANNEL)
            servo_front_shoulder_right_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_RIGHT_MIN_PULSE)
            servo_front_shoulder_right_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_SHOULDER_RIGHT_MAX_PULSE)

            if servo_front_shoulder_right_pca9685 == 1:
                self.servo_front_shoulder_right = servo.Servo(self.pca9685_1.channels[servo_front_shoulder_right_channel])
            else:
                self.servo_front_shoulder_right = servo.Servo(self.pca9685_2.channels[servo_front_shoulder_right_channel])
            self.servo_front_shoulder_right.set_pulse_width_range(min_pulse=servo_front_shoulder_right_min_pulse, max_pulse=servo_front_shoulder_right_max_pulse)

            servo_front_leg_right_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_RIGHT_PCA9685)
            servo_front_leg_right_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_RIGHT_CHANNEL)
            servo_front_leg_right_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_RIGHT_MIN_PULSE)
            servo_front_leg_right_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_LEG_RIGHT_MAX_PULSE)

            if servo_front_leg_right_pca9685 == 1:
                self.servo_front_leg_right = servo.Servo(self.pca9685_1.channels[servo_front_leg_right_channel])
            else:
                self.servo_front_leg_right = servo.Servo(self.pca9685_2.channels[servo_front_leg_right_channel])
            self.servo_front_leg_right.set_pulse_width_range(min_pulse=servo_front_leg_right_min_pulse, max_pulse=servo_front_leg_right_max_pulse)

            servo_front_feet_right_pca9685 = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_RIGHT_PCA9685)
            servo_front_feet_right_channel = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_RIGHT_CHANNEL)
            servo_front_feet_right_min_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_RIGHT_MIN_PULSE)
            servo_front_feet_right_max_pulse = Config().get(Config.MOTION_CONTROLLER_SERVOS_FRONT_FEET_RIGHT_MAX_PULSE)

            if servo_front_feet_right_pca9685 == 1:
                self.servo_front_feet_right = servo.Servo(self.pca9685_1.channels[servo_front_feet_right_channel])
            else:
                self.servo_front_feet_right = servo.Servo(self.pca9685_2.channels[servo_front_feet_right_channel])
            self.servo_front_feet_right.set_pulse_width_range(min_pulse=servo_front_feet_right_min_pulse, max_pulse=servo_front_feet_right_max_pulse)

        if self.arm_is_enabled:

            servo_arm_rotation_pca9685 = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_ROTATION_PCA9685)
            servo_arm_rotation_channel = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_ROTATION_CHANNEL)
            servo_arm_rotation_min_pulse = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_ROTATION_MIN_PULSE)
            servo_arm_rotation_max_pulse = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_ROTATION_MAX_PULSE)

            if servo_arm_rotation_pca9685 == 1:
                self.servo_arm_rotation = servo.Servo(self.pca9685_1.channels[servo_arm_rotation_channel])
            else:
                self.servo_arm_rotation = servo.Servo(self.pca9685_2.channels[servo_arm_rotation_channel])
            self.servo_arm_rotation.set_pulse_width_range(min_pulse=servo_arm_rotation_min_pulse, max_pulse=servo_arm_rotation_max_pulse)

            servo_arm_lift_pca9685 = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_LIFT_PCA9685)
            servo_arm_lift_channel = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_LIFT_CHANNEL)
            servo_arm_lift_min_pulse = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_LIFT_MIN_PULSE)
            servo_arm_lift_max_pulse = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_LIFT_MAX_PULSE)

            if servo_arm_lift_pca9685 == 1:
                self.servo_arm_lift = servo.Servo(self.pca9685_1.channels[servo_arm_lift_channel])
            else:
                self.servo_arm_lift = servo.Servo(self.pca9685_2.channels[servo_arm_lift_channel])
            self.servo_arm_lift.set_pulse_width_range(min_pulse=servo_arm_lift_min_pulse, max_pulse=servo_arm_lift_max_pulse)

            servo_arm_range_pca9685 = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_RANGE_PCA9685)
            servo_arm_range_channel = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_RANGE_CHANNEL)
            servo_arm_range_min_pulse = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_RANGE_MIN_PULSE)
            servo_arm_range_max_pulse = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_RANGE_MAX_PULSE)

            if servo_arm_range_pca9685 == 1:
                self.servo_arm_range = servo.Servo(self.pca9685_1.channels[servo_arm_range_channel])
            else:
                self.servo_arm_range = servo.Servo(self.pca9685_2.channels[servo_arm_range_channel])
            self.servo_arm_range.set_pulse_width_range(min_pulse=servo_arm_range_min_pulse, max_pulse=servo_arm_range_max_pulse)

            servo_arm_cam_tilt_pca9685 = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_CAM_TILT_PCA9685)
            servo_arm_cam_tilt_channel = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_CAM_TILT_CHANNEL)
            servo_arm_cam_tilt_min_pulse = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_CAM_TILT_MIN_PULSE)
            servo_arm_cam_tilt_max_pulse = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_CAM_TILT_MAX_PULSE)

            if servo_arm_cam_tilt_pca9685 == 1:
                self.servo_arm_cam_tilt = servo.Servo(self.pca9685_1.channels[servo_arm_cam_tilt_channel])
            else:
                self.servo_arm_cam_tilt = servo.Servo(self.pca9685_2.channels[servo_arm_cam_tilt_channel])
            self.servo_arm_cam_tilt.set_pulse_width_range(min_pulse=servo_arm_cam_tilt_min_pulse, max_pulse=servo_arm_cam_tilt_max_pulse)
