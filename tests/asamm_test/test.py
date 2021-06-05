from asamm.ichecker import IChecker
from utils.handlers import coroutine, AllExceptionsHandled


@AllExceptionsHandled(logged_call=True)
class MapperChecker(IChecker):
    """
    Класс содержит комплекс проверок перед
    блоком 'Mapper'
    """

    def run_all_checks(self, data_for_checks):
        super().run_all_checks(data_for_checks)
        return self.check_res

    @coroutine
    def check1(self, target=None):
        while True:
            s = yield
            self.check_res = s
            print(f"Check1 Get {s}")
            if target:
                target.send(s * s)


    @coroutine
    def check2(self, target=None):
        """
        Проверка чек1
        """
        while True:
            s = yield
            print(f"Check2 Get {s}")
            self.check_res = s
            if target:
                target.send(s * s)

    @coroutine
    def check3(self, target=None):
        while True:
            s = yield
            self.check_res = s
            print(f"Check3 Get {s}")
            if target:
                target.send(s * s)


if __name__ == '__main__':

    def f():
        yield 12


    v = list(f())
    print(v)
