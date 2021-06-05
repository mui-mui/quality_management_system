from abc import ABC, abstractmethod, abstractproperty
from typing import Deque
from utils.logger import LoggingMixin


class IProducer(ABC, LoggingMixin):
    _observers = {}

    def attach(self, observer: 'IObserver'):
        if not self._observers.get(name := self.__class__.__name__):
            self._observers[name] = list()
        self._observers[name].append(observer)
        self.info(f"Объект '{observer.__class__.__name__}' подписался на объект '{name}'")

    def detach(self, observer: 'IObserver'):
        raise NotImplemented()

    @abstractmethod
    def notify(self):
        for observer in self._observers[self.__class__.__name__]:
            self.info(
                f"Объект '{observer.__class__.__name__}' будет оповещен объектом '{self.__class__.__name__}'")
            observer.update(self)


class IObserver(ABC):
    @abstractmethod
    def update(self, producer: IProducer):
        pass


class ISystemNode(IProducer, IObserver):

    @abstractmethod
    def get_messages_queue(self) -> Deque:
        pass

    @abstractmethod
    def notify(self):
        super().notify()

    @abstractmethod
    def update(self, producer: IProducer):
        pass

    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplemented()





'''

class Producer(IProducer):
    def notify(self):
        super().notify()

    def test(self):
        print(f"Запуск оповещения {self.__class__.__name__}")
        self.notify()


class Observer(IObserver):
    name : str
    def update(self, producer: IProducer):
        print(f"Оповещение прошло для объекта {self.__class__.__name__}.{self.name} оповещал объект: {producer.__class__.__name__}")


if __name__ == '__main__':
    producer = Producer()
    observer1 = Observer()
    observer1.name = "observer1"

    observer2 = Observer()
    observer2.name = "observer2"

    producer.attach(observer1)
    producer.attach(observer2)

    producer.test()
'''
