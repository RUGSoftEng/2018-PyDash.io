"""
Logger object will log messages and errors to date-stamped '.log' files in the /logs directory of the project. Simply
import the class and use it to log messages.
"""

import logging
import os

from datetime import datetime


class Logger:
    def __init__(self, name=__name__):
        """
        Sets up default logging utility for logger object
        :param: name: namespace where you want the logger to be. Suggested value = __name__. Defaults to
        'pydash_app.impl.logger'.
        """
        logging.basicConfig(level=logging.INFO)

        self._default_logger = logging.getLogger(name)
        self._default_handler = logging.FileHandler(os.getcwd() + '/logs/' + str(datetime.today().date()) + '.log')
        self._default_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        self._default_handler.setFormatter(self._default_formatter)
        self._default_logger.addHandler(self._default_handler)

    def _log(self, msg, level):
        """
        Helper function to abstract setting the filename with each call. This is done by removing the current
        FileHandler and setting a new one up with the correct path.
        :param: msg: the message to be logged.
        :param: level: the level at which the message will be logged.
        """
        self._default_logger.removeHandler(self._default_handler)
        self._default_handler = logging.FileHandler(os.getcwd() + '/logs/' + str(datetime.today().date()) + '.log')

        self._default_handler.setFormatter(self._default_formatter)
        self._default_logger.addHandler(self._default_handler)

        # Log at correct level
        if level == logging.DEBUG:
            self._default_logger.debug(msg)

        if level == logging.INFO:
            self._default_logger.info(msg)

        if level == logging.WARNING:
            self._default_logger.warning(msg)

        if level == logging.ERROR:
            self._default_logger.error(msg)

    def debug(self, msg):
        """
        Takes a message and logs it at the logging.DEBUG level
        :param: msg: the message to be logged
        """
        self._log(msg, logging.DEBUG)

    def info(self, msg):
        """
        Takes a message and logs it at the logging.INFO level
        :param: msg: the message to be logged
        """
        self._log(msg, logging.INFO)

    def warning(self, msg):
        """
        Takes a message and logs it at the logging.WARN level
        :param: msg: the message to be logged
        """
        self._log(msg, logging.WARNING)

    def error(self, msg):
        """
        Takes a message and logs it at the logging.ERROR level
        :param: msg: the message to be logged
        """
        self._log(msg, logging.ERROR)
