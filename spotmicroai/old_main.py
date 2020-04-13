#!/usr/bin/env python3

import sys

from spotmicroai.utilities.log import Logger

import multiprocessing

from spotmicroai.motion_controller.motion_controller import MotionController
from spotmicroai.remote_controller.remote_controller import RemoteControllerController

log = Logger().setup_logger()


def process_motion_controller(communication_queues):
    motion = MotionController(communication_queues)
    motion.do_process_events_from_queues()


def process_remote_controller_controller(communication_queues):
    remote_controller = RemoteControllerController(communication_queues)
    remote_controller.do_process_events_from_queues()


def create_controllers_queues():
    communication_queues = {'motion_controller': multiprocessing.Queue(1)}

    log.info('Created the communication queues: ' + ', '.join(communication_queues.keys()))

    return communication_queues


def close_controllers_queues(communication_queues):
    log.info('Closing controller queues')

    for queue in communication_queues.items():
        queue.close()
        queue.join_thread()


def main():
    communication_queues = create_controllers_queues()

    # Start the motion controller
    # Moves the servos
    motion_controller = multiprocessing.Process(target=process_motion_controller, args=(communication_queues,))
    motion_controller.daemon = True

    # Activate Bluetooth controller
    # Let you move the dog using the bluetooth paired device
    remote_controller_controller = multiprocessing.Process(target=process_remote_controller_controller,
                                                           args=(communication_queues,))
    remote_controller_controller.daemon = True

    # Start the threads, queues messages are produced and consumed in those
    motion_controller.start()
    remote_controller_controller.start()

    if not motion_controller.is_alive():
        log.error("SpotMicro can't work without motion_controller")
        sys.exit(1)

    if not remote_controller_controller:
        log.error("SpotMicro can't work without remote_controller_controller")
        sys.exit(1)

    # Make sure the thread/process ends
    motion_controller.join()
    remote_controller_controller.join()

    close_controllers_queues(communication_queues)


if __name__ == '__main__':
    log.info('SpotMicro starting...')

    try:
        main()

    except KeyboardInterrupt:
        log.info('Terminated due Control+C was pressed')

    else:
        log.info('Normal termination')
