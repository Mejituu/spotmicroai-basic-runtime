import signal
import RPi.GPIO as GPIO
import sys
from spotmicro.utilities.log import Logger
from spotmicro.utilities.config import Config

log = Logger().setup_logger('Abort controller')


class AbortController:
    gpio_port = None

    def __init__(self, communication_queues):

        try:

            log.debug('Starting controller...')

            signal.signal(signal.SIGINT, self.exit_gracefully)
            signal.signal(signal.SIGTERM, self.exit_gracefully)

            self.gpio_port = Config().get('abort_controller[0].gpio_port')

            # Abort mechanism
            GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD
            GPIO.setup(self.gpio_port, GPIO.OUT)
            self._abort_queue = communication_queues['abort_controller']
            self._lcd_screen_queue = communication_queues['lcd_screen_controller']

            self._lcd_screen_queue.put('abort_controller OK')

            log.info('Controller started')

        except Exception as e:
            log.error('GPIO problem detected')
            self._lcd_screen_queue.put('abort_controller NOK')
            sys.exit(1)

    def exit_gracefully(self, signum, frame):
        log.info('Terminated')
        sys.exit(0)

    def do_process_events_from_queue(self):

        try:
            self.activate_servos()

            while True:
                event = self._abort_queue.get()

                if event == 'activate_servos':
                    self.activate_servos()

                if event == 'abort':
                    self.abort()

        except Exception as e:
            log.error('Unknown problem with the GPIO detected', e)

    def activate_servos(self):
        # GPIO.output(self.gpio_port, 1)  # Set GPIO pin value to 1/GPIO.HIGH/True
        pass

    def abort(self):
        # GPIO.output(self.gpio_port, 0)  # set GPIO pin value to 0/GPIO.LOW/False
        pass
