import sqlalchemy

from utils.executor.sql_caller.sql_engine.iengine import ISqlEngine
from sqlalchemy import create_engine


class SqlAlchemyMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Данная реализация не учитывает возможное изменение передаваемых
        аргументов в `__init__`.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class SqlAlchemyEngine(ISqlEngine):

    __metaclass__ = SqlAlchemyMeta

    def __init__(self, conn_string):
        self.conn_string = conn_string
        self.ctx = self.create_context()

    @property
    def context(self) -> sqlalchemy.engine.Engine:
        return self.ctx

    def create_context(self):
        return create_engine(self.conn_string)
