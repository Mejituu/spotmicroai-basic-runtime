import json
import sys
import os
from spotmicro.utilities.log import Logger
import jmespath  # http://jmespath.org/tutorial.html
import shutil
from pathlib import Path

log = Logger().setup_logger('Configuration')


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(metaclass=Singleton):
    values = {}

    def __init__(self):

        try:
            log.debug('Loading configuration...')

            self.load_config()
            self.list_modules()

        except Exception as e:
            log.error('Problem while loading the configuration file', e)

    def load_config(self):
        try:
            if not os.path.exists(str(Path.home()) + '/spotmicroai.json'):
                shutil.copyfile(str(Path.home()) + '/spotmicroai/spotmicroai.default', str(Path.home()) + '/spotmicroai.json')

            with open(str(Path.home()) + '/spotmicroai.json') as json_file:
                self.values = json.load(json_file)
                # log.debug(json.dumps(self.values, indent=4, sort_keys=True))

        except Exception as e:
            log.error("Configuration file don't exist or is not a valid json, aborting.")
            sys.exit(1)

    def list_modules(self):
        log.info('Detected configuration for the modules: ' + ', '.join(self.values.keys()))

    def save_config(self):
        try:
            with open('~/spotmicroai.json', 'w') as outfile:
                json.dump(self.values, outfile)
        except Exception as e:
            log.error("Problem saving the configuration file", e)

    def get(self, search_pattern):
        log.debug(search_pattern + ': ' + str(jmespath.search(search_pattern, self.values)))
        return jmespath.search(search_pattern, self.values)
