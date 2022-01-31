import inspect
import logging
from pathlib import Path


class Logger:
    ROOT_PATH = str(Path(__file__).parent.parent)

    def get_logger(self):
        logger_name = inspect.stack()[1][3]
        logger = logging.getLogger(logger_name)
        filehandler = logging.FileHandler('logfile.log')
        log_format = logging.Formatter("%(asctime)s :%(levelname)s :%(name)s :%(message)s")
        filehandler.setFormatter(log_format)
        logger.addHandler(filehandler)
        logger.setLevel(logging.DEBUG)
        return logger
