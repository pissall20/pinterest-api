import logging
import os


class Logger(object):
    """
    Creates a logger instance when called inside a file/class
    examples:
    # >>> from logger import Logger
    # >>> logger1 = Logger(self.__class__.__name__).get()
    # >>> logger2 = Logger('example').get()
    """
    LOGGING_DIR = "logs/"

    def __init__(self, name):
        """
        Creates a logger instance.
        :param name: Log file name (The logging module automatically appends a `.log` suffix to the name)
        """
        # Optional replacement for .log suffix if mistakenly added
        name = name.replace(".log", "")
        logger = logging.getLogger(f"logs.{name}")  # logs is a namespace
        logger.setLevel(logging.ERROR)
        if not logger.handlers:
            file_name = os.path.join(self.LOGGING_DIR, f"{name}.log")
            handler = logging.FileHandler(file_name)
            formatter = logging.Formatter(
                "%(asctime)s %(levelname)s:%(name)s %(message)s"
            )
            handler.setFormatter(formatter)
            handler.setLevel(logging.ERROR)
            logger.addHandler(handler)
        self._logger = logger

    def get(self):
        return self._logger
