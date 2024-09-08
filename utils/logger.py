# TODO: add the option to add params to logs.
import logging
import sys

from utils.color_formatter import ColorFormatter


class JarvisLogger:

    def __init__(self, logger_name: str):
        super().__init__()
        # Create a custom logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)  # Set the minimum log level

        # Create handlers
        console_handler = logging.StreamHandler(sys.stdout)  # Log to console

        # Set level for handlers
        console_handler.setLevel(logging.DEBUG)

        # Apply colored formatter for console logs
        color_formatter = ColorFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(color_formatter)

        # Apply normal formatter for file logs

        # Add handlers to the logger
        self.logger.addHandler(console_handler)

    def info(self, message: str, params: dict = None):
        self.logger.info(message)

    def error(self, message: str, params: dict = None):
        self.logger.error(message)


if __name__ == '__main__':
    logger = JarvisLogger(logger_name="test")
    logger.info("hello world")
    logger.error("this is an error")
