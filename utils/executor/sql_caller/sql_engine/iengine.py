from abc import ABC, abstractproperty, abstractmethod


class ISqlEngine(ABC):
    """
    Интерфейс для создания контекста к различным БД
    """
    @abstractproperty
    def context(self):
        pass

    @abstractmethod
    def create_context(self, *args, **kwargs):
        pass
