import functools
import sys
import traceback
from functools import wraps
from typing import List


from utils.logger import LoggingMixin


class AllExceptionsHandled(LoggingMixin):
    EXCEPTION_TYPE = Exception

    def __init__(self, logged_call=False, handler=None):
        """
        Декоратор для обработки исключений. По-умолчанию ловит все исключения,
        чтобы исключение не было поймано, следует применить декоратор AllExceptionsHandled.not_handled(<класс_исключения>)
        :param logged_call: флаг логгирования запуска и завершения методов
        :param handler: функция-обработчик возникшего исключения, необязательный аргумент
        """
        self.handler = handler
        self.logged_call = logged_call

    def __call__(self, klass, *args, **kwargs):
        self.klass = klass
        return self._klass_wrapper

    def _klass_wrapper(self, *args, **kwargs):
        for attr_name in filter(lambda at_name: not str.startswith(at_name, '_'), self.klass.__dict__):
            attr = getattr(self.klass, attr_name)
            if hasattr(attr, '_not_handled') and attr._not_handled:
                func = self._exception_handler(attr._non_exceptions)
                setattr(self.klass, attr_name, func(attr))
            else:
                func = self._exception_handler()
                setattr(self.klass, attr_name, func(attr))
        functools.update_wrapper(self, self.klass)
        return self.klass(*args, **kwargs)

    def _exception_handler(self, non_exceptions: List = None):
        def decorator(method):
            @wraps(method)
            def wrapper(*args, **kwargs):
                try:
                    if self.logged_call:
                        self.info(
                            f"Запуск метода '{method.__name__}' {'({0})'.format(method.__doc__.strip()) if method.__doc__ else ''} ")
                    res = method(*args, **kwargs)
                    #if self.logged_call:
                    #    self.info(f"Метод '{method.__name__} выполнен успешно.")
                    return res
                except self.EXCEPTION_TYPE or GeneratorExit as e:
                    if non_exceptions is not None:
                        for ex in non_exceptions:
                            if isinstance(e, ex): raise e
                    self.error(f"Произошло исключение: {traceback.format_exc()}. Работа программы будет остановлена.")
                    #print(f"Произошло исключение: {e}. Работа программы будет остановлена.")
                    if self.handler is not None:
                        self.handler(*args, **kwargs)
                    sys.exit(-1)

            return wrapper

        return decorator


    @staticmethod
    def not_handled(*exceptions: EXCEPTION_TYPE):
        """
        Метод проброса исключения
        :param exceptions: исключения, которые не нужно отлавливать
        :return:
        """

        def decorator(method):

            @wraps(method)
            def wrapper(self, *args, **kwargs):
                return method(self, *args, **kwargs)

            wrapper._not_handled = True
            wrapper._non_exceptions = list(exceptions)
            return wrapper

        return decorator



"""
@AllExceptionsHandled(logged_call=True)
class AllExceptionsHandled_test(LoggingMixin):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    #@AllExceptionsHandled.not_handled(TypeError)
    def sum(self, x, z):
        return x + z

    #@AllExceptionsHandled.not_handled(ZeroDivisionError)
    def div(self):
        self.info("Деление...")
        return self.a / self.b


    @classmethod
    def create(cls):
        return cls

if __name__ == '__main__':
    t = AllExceptionsHandled_test(10, 2)
    print(t.sum(3, 5))
    print(t.div())
    n_c = AllExceptionsHandled_test.create()

    #print(t.div._not_handled)
    # print(t.div._not_handled)

"""

