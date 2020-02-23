#!/usr/bin/env python3

import sys, os, signal

from spotmicro.utilities.log import Logger
from spotmicro.utilities.config import Config

import multiprocessing
from multiprocessing.managers import BaseManager

from queue import LifoQueue

from spotmicro.motion_controller.motion_controller import MotionController
from spotmicro.abort_controller.abort_controller import AbortController
from spotmicro.lcd_screen_controller.lcd_screen_controller import LCDScreenController
from spotmicro.remote_controller.remote_controller import RemoteControllerController

log = Logger().setup_logger()


def process_abort_controller(communication_queues):
    abort = AbortController(communication_queues)
    abort.do_process_events_from_queue()


def process_motion_controller(communication_queues):
    motion = MotionController(communication_queues)
    motion.do_process_events_from_queues()


def process_remote_controller_controller(communication_queues):
    remote_controller = RemoteControllerController(communication_queues)
    remote_controller.do_process_events_from_queues()


# Optional
def process_output_lcd_screen_controller(communication_queues):
    lcd_screen = LCDScreenController(communication_queues)
    lcd_screen.do_process_events_from_queue()


# create manager that knows how to create and manage LifoQueues
# class MyManager(BaseManager):
#    pass


def create_controllers_queues():
    # https://docs.python.org/3/library/queue.html
    # The reason we use queues for inter process communication is because simplicity
    # Why we use multiple queues? Because we limit the number of messages on them and
    # some sensors read and update them at very high frequency, other don't. Having a sole queue
    # makes the high frequency update controllers to wipe out the slow ones messages.
    # Get and Put methods handle the locks via optional parameter block=True

    # Queues must be 10ish, controller will flood with orders, we use .get(block true) to avoid
    # this we read as we can process

    # MyManager.register('LifoQueue', LifoQueue)
    # manager = MyManager()
    # manager.start()

    communication_queues = {'abort_controller': multiprocessing.Queue(10),
                            # 'motion_controller': manager.LifoQueue(),
                            'motion_controller': multiprocessing.Queue(1),
                            'lcd_screen_controller': multiprocessing.Queue(10)}

    log.info('Created the communication queues: ' + ', '.join(communication_queues.keys()))

    return communication_queues


def close_controllers_queues(communication_queues):
    log.info('Closing controller queues')

    for queue in communication_queues.items():
        queue.close()
        queue.join_thread()


def main():

    communication_queues = create_controllers_queues()

    # Start the abort controller
    # 0E port from PCA9685 must be HIGH
    abort_controller = multiprocessing.Process(target=process_abort_controller, args=(communication_queues,))
    abort_controller.daemon = True  # The daemon process will continue to run as long as the main process is executing
    # and it will terminate after finishing its execution or when the main program would be killed.

    # Start the motion controller
    # Process/Thread, listening the events QUEUE for orders
    motion_controller = multiprocessing.Process(target=process_motion_controller, args=(communication_queues,))
    motion_controller.daemon = True  # The daemon process will continue to run as long as the main process is executing
    # and it will terminate after finishing its execution or when the main program would be killed.

    # Activate Bluetooth controller
    # Capture the buttons from the controller and generate events for the QUEUE
    remote_controller_controller = multiprocessing.Process(target=process_remote_controller_controller,
                                                           args=(communication_queues,))
    remote_controller_controller.daemon = True

    # Activate Screen
    # Show communication on it about the status
    lcd_screen_controller = multiprocessing.Process(target=process_output_lcd_screen_controller,
                                                    args=(communication_queues,))
    lcd_screen_controller.daemon = True

    # Start the threads queue processing
    abort_controller.start()
    motion_controller.start()
    remote_controller_controller.start()
    lcd_screen_controller.start()

    if not abort_controller.is_alive():
        log.error("SpotMicro can't work without abort_controller")
        sys.exit(1)

    if not motion_controller.is_alive():
        log.error("SpotMicro can't work without motion_controller")
        sys.exit(1)

    if not remote_controller_controller:
        log.error("SpotMicro can't work without remote_controller_controller")
        sys.exit(1)

    # make sure the thread/process ends
    abort_controller.join()
    motion_controller.join()
    remote_controller_controller.join()
    lcd_screen_controller.join()

    close_controllers_queues(communication_queues)


if __name__ == '__main__':
    log.info('SpotMicro starting...')

    try:
        main()

    # except Exception as e:
    #    log.error('Terminated due error')

    except KeyboardInterrupt:
        log.info('Terminated due Control+C was pressed')

    else:
        log.info('Normal termination')
