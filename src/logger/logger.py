import logging
import ntpath
import os

from config import Config


class Logger:
    @staticmethod
    def __config_library_loggers() -> None:
        """
        Configures the loggers for the libraries used in the project
        """
        pass

    @staticmethod
    def get_logger(filepath: str) -> logging.Logger:
        Logger.__config_library_loggers()  # Configuring library loggers

        filename = ntpath.basename(filepath)  # Get filename from filepath, and removes .py from the end
        log_save_path = os.path.join(Config.LOG_DIR.value, f"{filename}.log")

        # Logger configuration
        logging.basicConfig(
            level=Config.LOGGING_LEVEL.value,
        )

        logger = logging.getLogger(filename)
        handler = logging.FileHandler(filename=log_save_path, mode="w")
        formatter = logging.Formatter(
            fmt='{:<15}{:<15}{:<15}{:<15}'.format('%(asctime)s', '%(levelname)s', '%(filename)s', '%(message)s'),
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger
