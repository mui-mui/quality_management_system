from typing import Callable

import pandas as pd
from utils.executor.sql_caller.sql_engine import ISqlEngine, SqlAlchemyEngine
from utils.handlers import AllExceptionsHandled
from utils.executor.call_result import call_result
from utils.executor.iblockcaller import IBlockCaller


class SqlBlockCaller(IBlockCaller):
    """
    Исполнитель блока типа 'QUERY' из конфигурации
    """
    sql_engine: ISqlEngine
    executor_func: Callable  # функция выполняющий запрос к бд

    def __init__(self, sql_engine: ISqlEngine, executor_func: Callable):
        self.sql_engine = sql_engine
        self.executor_func = executor_func

    def call(self, id_: str, name: str, query: str, transform_script: Callable = None):
        """
        Выполнение запроса к бд
        """
        self.info(f"Выполнение запроса '{name}'...")
        res = self.executor_func(query)

        return call_result(
            id=id_,
            name=name,
            result=transform_script(res) if transform_script else res,
            error=f"Запрос {name} вернул null" if res.empty else None)  # TODO: Пересмотреть 'res.empty'

    @classmethod
    def create_sqlalchemy_pandas_executor(cls, conn_string):
        klass = cls(SqlAlchemyEngine(conn_string).context, pd.read_sql)
        return klass
