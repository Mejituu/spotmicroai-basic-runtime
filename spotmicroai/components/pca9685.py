from adafruit_motor import servo


class PCA9685:
    pca9685 = None

    servo_rear_left_shoulder = None
    servo_rear_left_knee = None
    servo_rear_left_feet = None
    servo_rear_right_shoulder = None
    servo_rear_right_knee = None
    servo_rear_right_feet = None
    servo_front_left_shoulder = None
    servo_front_left_knee = None
    servo_front_left_feet = None
    servo_front_right_shoulder = None
    servo_front_right_knee = None
    servo_front_right_feet = None

    def __init__(self, bus_i2c):
        pca9685 = PCA9685(bus_i2c, address=config.pca9685_address, reference_clock_speed=config.pca9685_reference_clock_speed)
        pca9685.frequency = config.pca9685_frequency

    def setup(self):
        servo_rear_left_shoulder = self.setup_servo('servo_rear_left_shoulder')
        servo_rear_left_knee = self.setup_servo('servo_rear_left_knee')
        servo_rear_left_feet = self.setup_servo('servo_rear_left_feet')

        servo_rear_right_shoulder = self.setup_servo('servo_rear_right_shoulder')
        servo_rear_right_knee = self.setup_servo('servo_rear_right_knee')
        servo_rear_right_feet = self.setup_servo('servo_rear_right_feet')

        servo_front_left_shoulder = self.setup_servo('servo_front_left_shoulder')
        servo_front_left_knee = self.setup_servo('servo_front_left_knee')
        servo_front_left_feet = self.setup_servo('servo_front_left_feet')

        servo_front_right_shoulder = self.setup_servo('servo_front_right_shoulder')
        servo_front_right_knee = self.setup_servo('servo_front_right_knee')
        servo_front_right_feet = self.setup_servo('servo_front_right_feet')

    def setup_servo(self, name):
        servo = servo.Servo(self.pca9685.channels[config.get(name, channel)])
        servo.set_pulse_width_range(min_pulse=config.get(name, min_pulse), max_pulse=config.get(name, max_pulse))
        servo.angle = config.get(name, angle)

        return servo
