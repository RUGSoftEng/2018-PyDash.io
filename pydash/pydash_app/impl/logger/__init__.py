"""
Creates a default_logger for use in the entire project. This logger will log messages and errors to dated .log files in
the /logs directory of the project.
"""
import logging
import datetime
import pathlib
import os

"""Default settings"""
logging.basicConfig(level=logging.INFO)

default_logger = logging.getLogger(__name__)
default_handler = logging.FileHandler(os.getcwd() + '/logs/' + str(datetime.datetime.today().date()) + '.log')
default_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

default_handler.setFormatter(default_formatter)
default_logger.addHandler(default_handler)

def log():

    pass
