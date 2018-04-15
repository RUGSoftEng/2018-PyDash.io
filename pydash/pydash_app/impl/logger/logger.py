import logging
import pathlib
import os

from datetime import datetime


class Logger:
    def __init__(self):
        """Sets up default logging utility for logger object"""
        logging.basicConfig(level=logging.INFO)

        self._default_logger = logging.getLogger(__name__)
        self._default_handler = logging.FileHandler(os.getcwd() + '/logs/' + str(datetime.today().date()) + '.log')
        self._default_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self._default_handler.setFormatter(self._default_formatter)
        self._default_logger.addHandler(self._default_handler)

        self._default_logger.info('Initializing logger done')

    def _log(self, msg, level):
        """
        Helper function to abstract setting the filename with each call
        :msg: the message to be logged.
        :level: the level at which the message will be logged.
        """
        pass

    def debug(self, msg):
        """
        Takes a message and logs it at the logging.DEBUG level
        :msg: the message to be logged
        """
        pass

    def info(self, msg):
        """
        Takes a message and logs it at the logging.INFO level
        :msg: the message to be logged
        """
        pass

    def warn(self, msg):
        """
        Takes a message and logs it at the logging.WARN level
        :msg: the message to be logged
        """
        pass

    def error(self, msg):
        """
        Takes a message and logs it at the logging.ERROR level
        :msg: the message to be logged
        """
        pass
