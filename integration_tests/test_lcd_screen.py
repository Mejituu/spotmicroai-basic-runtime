#!/usr/bin/env python3

from spotmicro.lcd_screen_controller.lcd_screen_controller import LCDScreenController
import spotmicro.utilities.log as logger

log = logger.setup_logger('IntegrationTest_LCDScreen')

if __name__ == '__main__':
    i2c_address = 41

    try:

        lcd_screen = LCDScreenController(None)

        lcd_screen.clear()
        lcd_screen.write_first_line()
        lcd_screen.write_second_line()
        lcd_screen.turn_off()
        lcd_screen.turn_on()

    except:
        print('Error with LCDScreenController')
