from abc import ABC, abstractmethod
from utils.executor.call_result import call_result

from utils.logger import LoggingMixin


class IBlockCaller(ABC, LoggingMixin):
    """
    Интерфейс исполнителя блока
    """
    @abstractmethod
    def call(self, *args, **kwargs) -> call_result:
        pass
