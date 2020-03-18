from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

from spotmicroai.utilities.log import Logger
from spotmicroai.utilities.config import Config

log = Logger().setup_logger('Motion controller setup')


class MotionController:
    boards = 1

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

    servo_arm_rotation = None
    servo_arm_rotation_pca9685 = None
    servo_arm_rotation_channel = None
    servo_arm_rotation_min_pulse = None
    servo_arm_rotation_max_pulse = None
    servo_arm_rotation_rest_angle = None

    servo_arm_lift = None
    servo_arm_lift_pca9685 = None
    servo_arm_lift_channel = None
    servo_arm_lift_min_pulse = None
    servo_arm_lift_max_pulse = None
    servo_arm_lift_rest_angle = None

    servo_arm_range = None
    servo_arm_range_pca9685 = None
    servo_arm_range_channel = None
    servo_arm_range_min_pulse = None
    servo_arm_range_max_pulse = None
    servo_arm_range_rest_angle = None

    servo_arm_cam_tilt = None
    servo_arm_cam_tilt_pca9685 = None
    servo_arm_cam_tilt_channel = None
    servo_arm_cam_tilt_min_pulse = None
    servo_arm_cam_tilt_max_pulse = None
    servo_arm_cam_tilt_rest_angle = None

    def __init__(self):
        pass

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

        self.servo_arm_rotation_pca9685 = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_ROTATION_PCA9685)
        self.servo_arm_rotation_channel = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_ROTATION_CHANNEL)
        self.servo_arm_rotation_min_pulse = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_ROTATION_MIN_PULSE)
        self.servo_arm_rotation_max_pulse = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_ROTATION_MAX_PULSE)
        self.servo_arm_rotation_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_ROTATION_REST_ANGLE)

        self.servo_arm_lift_pca9685 = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_LIFT_PCA9685)
        self.servo_arm_lift_channel = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_LIFT_CHANNEL)
        self.servo_arm_lift_min_pulse = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_LIFT_MIN_PULSE)
        self.servo_arm_lift_max_pulse = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_LIFT_MAX_PULSE)
        self.servo_arm_lift_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_LIFT_REST_ANGLE)

        self.servo_arm_range_pca9685 = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_RANGE_PCA9685)
        self.servo_arm_range_channel = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_RANGE_CHANNEL)
        self.servo_arm_range_min_pulse = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_RANGE_MIN_PULSE)
        self.servo_arm_range_max_pulse = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_RANGE_MAX_PULSE)
        self.servo_arm_range_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_RANGE_REST_ANGLE)

        self.servo_arm_cam_tilt_pca9685 = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_CAM_TILT_PCA9685)
        self.servo_arm_cam_tilt_channel = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_CAM_TILT_CHANNEL)
        self.servo_arm_cam_tilt_min_pulse = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_CAM_TILT_MIN_PULSE)
        self.servo_arm_cam_tilt_max_pulse = Config().get(Config.ARM_CONTROLLER_SERVOS_ARM_CAM_TILT_MAX_PULSE)
        self.servo_arm_cam_tilt_rest_angle = Config().get(Config.MOTION_CONTROLLER_SERVOS_ARM_CAM_TILT_REST_ANGLE)

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

        if self.servo_arm_rotation_pca9685 == 1:
            self.servo_arm_rotation = servo.Servo(self.pca9685_1.channels[self.servo_arm_rotation_channel])
        else:
            self.servo_arm_rotation = servo.Servo(self.pca9685_2.channels[self.servo_arm_rotation_channel])
        self.servo_arm_rotation.set_pulse_width_range(min_pulse=self.servo_arm_rotation_min_pulse, max_pulse=self.servo_arm_rotation_max_pulse)

        if self.servo_arm_lift_pca9685 == 1:
            self.servo_arm_lift = servo.Servo(self.pca9685_1.channels[self.servo_arm_lift_channel])
        else:
            self.servo_arm_lift = servo.Servo(self.pca9685_2.channels[self.servo_arm_lift_channel])
        self.servo_arm_lift.set_pulse_width_range(min_pulse=self.servo_arm_lift_min_pulse, max_pulse=self.servo_arm_lift_max_pulse)

        if self.servo_arm_range_pca9685 == 1:
            self.servo_arm_range = servo.Servo(self.pca9685_1.channels[self.servo_arm_range_channel])
        else:
            self.servo_arm_range = servo.Servo(self.pca9685_2.channels[self.servo_arm_range_channel])
        self.servo_arm_range.set_pulse_width_range(min_pulse=self.servo_arm_range_min_pulse, max_pulse=self.servo_arm_range_max_pulse)

        if self.servo_arm_cam_tilt_pca9685 == 1:
            self.servo_arm_cam_tilt = servo.Servo(self.pca9685_1.channels[self.servo_arm_cam_tilt_channel])
        else:
            self.servo_arm_cam_tilt = servo.Servo(self.pca9685_2.channels[self.servo_arm_cam_tilt_channel])
        self.servo_arm_cam_tilt.set_pulse_width_range(min_pulse=self.servo_arm_cam_tilt_min_pulse, max_pulse=self.servo_arm_cam_tilt_max_pulse)
