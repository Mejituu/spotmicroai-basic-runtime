from spotmicroai.utilities.log import Logger

from spotmicroai.components.bus_i2c import BUSI2C
from spotmicroai.components.pca9685 import PCA9685
from spotmicroai.components.bluetooth_controller import BluetoothController

from spotmicroai.robot.robot import Robot

log = Logger().setup_logger('Motion controller')

if __name__ == '__main__':

    try:
        log.info('SpotMicro starting...')

        # I2C bus
        bus_i2c = BUSI2C()

        pca9685 = PCA9685(bus_i2c)

        bluetooth_controller = BluetoothController()

        robot = Robot(pca9685)

    except KeyboardInterrupt:
        log.info('Terminated due Control+C was pressed')

    else:
        log.info('Normal termination')
