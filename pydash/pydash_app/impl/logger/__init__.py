"""
Creates a default_logger for use in the entire project. This logger will log messages and errors to date-stamped .log
files in the /logs directory of the project.
"""
from .logger import Logger

logger = Logger()
logger.info('Initializing logger done')
