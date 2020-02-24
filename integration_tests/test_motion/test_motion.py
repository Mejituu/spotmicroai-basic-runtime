#!/home/pi/spotmicroai/venv/bin/python3 -u

# Example based from https://github.com/adafruit/Adafruit_CircuitPython_PCA9685/blob/master/examples/pca9685_servo.py
# Servo library used to simplify: https://github.com/adafruit/Adafruit_CircuitPython_Motor/blob/master/adafruit_motor/servo.py

# python3 -m venv venv --clear
# source venv/bin/activate
# curl https://bootstrap.pypa.io/get-pip.py | python
# pip install --upgrade pip
# pip install --upgrade setuptools
# python3 -m pip install smbus
# python3 -m pip install adafruit-circuitpython-motor
# python3 -m pip install adafruit-circuitpython-pca9685

# reference_clock_speed from: https://github.com/adafruit/Adafruit_CircuitPython_PCA9685/blob/master/examples/pca9685_calibration.py

import busio
from board import SCL, SDA
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
import time

try:

    i2c = busio.I2C(SCL, SDA)
    pca = PCA9685(i2c, address=0x40, reference_clock_speed=25000000)
    pca.frequency = 50

    servo_0 = servo.Servo(pca.channels[0])
    servo_0.set_pulse_width_range(min_pulse=500, max_pulse=2500)

    # Move by angle
    servo_0.angle = 90
    time.sleep(2)

    servo_0.angle = 100
    time.sleep(2)

    servo_0.angle = 90
    time.sleep(2)

    servo_0.angle = 80
    time.sleep(2)

finally:
    pca.deinit()
