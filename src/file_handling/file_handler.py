from abc import ABC, abstractmethod
from typing import Any

from src.logger.logger import Logger


class FileHandler(ABC):
    __file_path: str
    __logger: Logger

    def __init__(self, file_path: str, logger: Logger) -> None:
        self.file_path = file_path
        self.logger = logger

    @property
    def file_path(self) -> str:
        return self.__file_path

    @file_path.setter
    def file_path(self, file_path: str) -> None:
        if not file_path:
            raise TypeError("File path cannot be empty")

        self.__file_path = file_path

    @property
    @abstractmethod
    def file(self) -> Any:
        pass

    @file.setter
    @abstractmethod
    def file(self, file: Any) -> None:
        pass

    @property
    def logger(self) -> Logger:
        return self.__logger

    @logger.setter
    def logger(self, logger: Logger) -> None:
        if not logger:
            raise TypeError("Logger cannot be empty")

        self.__logger = logger

    @abstractmethod
    def _open(self) -> None:
        pass
