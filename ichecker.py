from abc import ABC, abstractmethod
from typing import Iterable


class IChecker(ABC):
    """
    Интерфейс для создания цепочи проверок
    Пример создания методов проверок для класса:
    @coroutine <-- объявить декоратор
    def check3(self, target=None): <-- атрибут target=None
       while True:
           s = yield
           self.check_result = s
           if target:
               target.send(s * s)
    """

    @abstractmethod
    def run_all_checks(self, data_for_checks):
        """
        Выполняет поиск всех методов в классе с декоратором 'coroutine'
        и выстаивает их в цепочку вызовов
        :param data_for_checks:
        :return:
        """
        checks = list()
        for func_name in filter(lambda name: not str.startswith(name, '_'), dir(self)):
            func = getattr(self, func_name)
            if hasattr(func, "isCoroutine") and func.isCoroutine:
                checks.append(func(checks[len(checks) - 1]) if checks else func())

        if checks:
            checks[len(checks) - 1].send(data_for_checks)
            [f.close() for f in checks] # завершить работу корутинов
        #raise Exception(f"Обработчиков для проверки в {self.__class__.__name__} не найдено!")


if __name__ == '__main__':
    print(IChecker.__doc__)