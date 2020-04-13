from spotmicroai.robot.leg import Leg


class Robot:

    leg_rear_left = None
    leg_rear_right = None
    leg_front_left = None
    leg_front_right = None

    def __init__(self, pca9685):

        self.leg_rear_left = Leg(pca9685.servo_rear_left_shoulder, pca9685.servo_rear_left_knee, pca9685.servo_rear_left_feet)
        self.leg_rear_right = Leg(pca9685.servo_rear_right_shoulder, pca9685.servo_rear_right_knee, pca9685.servo_rear_right_feet)
        self.leg_front_left = Leg(pca9685.servo_front_left_shoulder, pca9685.servo_front_left_knee, pca9685.servo_front_left_feet)
        self.leg_front_right = Leg(pca9685.servo_front_left_shoulder, pca9685.servo_front_left_knee, pca9685.servo_front_left_feet)

    def kinematics(self):
        pass