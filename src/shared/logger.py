from logging import DEBUG, Formatter, getLogger


class Logger:
    def __init__(self, name: str, level: int = DEBUG) -> None:
        self.logger = getLogger(name)
        self.logger.setLevel(level)
        self.formatter = Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

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
