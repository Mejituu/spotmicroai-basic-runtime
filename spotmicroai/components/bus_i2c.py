import busio
from board import SCL, SDA


class BUSI2C:

    def __init__(self):
        i2c = busio.I2C(SCL, SDA)
