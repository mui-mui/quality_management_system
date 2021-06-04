
class A:
    abc = 10
    """
    fewfefwe
    """
    def __new__(cls, *args, **kwargs):
        for attr_name in filter(lambda at_name: not str.startswith(at_name, '_'), cls.__dict__):
            attr = getattr(cls, attr_name)
            if callable(attr):
                attr.__doc__ = f"Запуск внешнего скрипта {attr.__name__}"
        return cls

    def __init__(self):
        self.a = 10
        self.b = 20

    def sum(self, name, arg1):
        return self.a + self.b


def test():
    for i in range(3):
        x = yield
        print(i, x)

if __name__ == '__main__':
    t = test()
    t.send(None)
    t.send(1)
    t.send(2)
    t.send(3)
    t.send(4)


