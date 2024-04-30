import sys
from logging import DEBUG, Formatter, StreamHandler, getLogger


class Logger:
    def __init__(self, name: str, level: int = DEBUG) -> None:
        self.logger = getLogger(name)
        self.logger.setLevel(level)
        self.formatter = Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        # Create a StreamHandler for stdout and add it to the logger
        handler = StreamHandler(sys.stdout)
        handler.setFormatter(self.formatter)
        self.logger.addHandler(handler)

    def exception(self, message: str) -> None:
        self.logger.exception("-" * 50)
        self.logger.exception(message)
        self.logger.exception("-" * 50)

    def info(self, message: str) -> None:
        self.logger.info("-" * 50)
        self.logger.info(message)
        self.logger.info("-" * 50)

    def error(self, message: str) -> None:
        self.logger.error("-" * 50)
        self.logger.error(message)
        self.logger.error("-" * 50)
