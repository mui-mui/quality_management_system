from abc import ABC, abstractmethod

from utils.executor.call_result import call_result
from utils.logger import LoggingMixin
from utils.executor.sql_caller import SqlBlockCaller
from utils.executor.script_caller import ScriptBlockCaller


class IExecutor(ABC, LoggingMixin):

    def execute(self, *args, **kwargs) -> call_result:
        executor = self.create_executor()
        res = executor.call(*args, **kwargs)
        return res

    @abstractmethod
    def create_executor(self):
        pass


class SqlExecutor(IExecutor):
    def __init__(self, connect_string: str):
        self.conn_str = connect_string

    def create_executor(self):
        return SqlBlockCaller.create_sqlalchemy_pandas_executor(self.conn_str)


class ScriptExecutor(IExecutor):

    def create_executor(self):
        return ScriptBlockCaller()
