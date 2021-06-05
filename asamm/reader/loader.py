from concurrent.futures import ThreadPoolExecutor
from typing import Iterable

from utils.executor import call_result
from utils.logger import LoggingMixin
from asamm import exception_handler
from utils.executor import *



class Loader(LoggingMixin):
    """
    Класс загрузки данных из БД и их трансформации по скриптам трансформации
    """

    def __init__(self, sql_executor: IExecutor, script_executor: IExecutor):
        self.sql_executor = sql_executor
        self.script_executor = script_executor

    def invoke(self, slq_block_items) -> Iterable[call_result]:
        """
        Загрузка из бд
        """

        with ThreadPoolExecutor(len(slq_block_items)) as executor:
            for item in executor.map(
                    lambda query: self.sql_executor.execute(id=query.id,
                                                            name=query.name,
                                                            query=query.query,
                                                            transform_script=self.script_executor.execute(
                                                                name=f"Трансформация для запроса '{query.name}'",
                                                                script_path=query.script,
                                                                func_name="main").result), slq_block_items):
                if item.error is not None:
                    self.warning(item.error)
                    raise RuntimeWarning()

                yield item
