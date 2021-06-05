from typing import List, Iterable, Deque
from collections import deque

from asamm import AsammConfiguration
from asamm.asamm_message import AsammMessage
from asamm.asamm_node import ISystemNode
from asamm.parse_config import ConfigSqlBlock
from asamm.parse_config import SqlBlockConfigParser
from asamm.reader.loader import Loader
from asamm.reader.contatenator import Concatenator
from utils.executor.call_result import call_result
from utils.config_reader import read_config
from utils.handlers import AllExceptionsHandled


@AllExceptionsHandled(logged_call=True)
class Reader(ISystemNode):
    """
    Класс-фасад формирует логику работы Reader системы АСАММ.
    """

    config = read_config(AsammConfiguration.READER_CONFIG)
    outgoing_data = deque()

    def __init__(self, loader: Loader):
        self.config_parser = SqlBlockConfigParser()
        self.loader = loader

    @property
    def get_messages_queue(self) -> Deque:
        return self.outgoing_data

    def notify(self):
        super().notify()

    def update(self, producer: ISystemNode):
        raise NotImplemented()

    def _get_load_config(self, load_config, piece_ids) -> List[ConfigSqlBlock]:
        """
        Выполняет конфигурацию sql запросов, вставляет в шаблон
        запроса список piece_id
        """
        for item in load_config:
            setup_query_script = self.loader.script_executor.execute(item.id, item.name, item.setup_query,
                                                                     "main").result
            item.query = setup_query_script(item.query, piece_ids)
        return load_config

    def _execute_preload_step(self, preload_config) -> Iterable[call_result]:
        """
        Выполняет шаг предзагрузки PIECE_ID, для
        формирования запросов для шага 'load'
        :return:
        """
        return self.loader.invoke(preload_config)

    def _execute_load_step(self, load_config) -> Iterable:
        for result in self.loader.invoke(load_config):
            yield result

    def _execute_join(self, join_config, results: List):
        concat = Concatenator(
            func_concat=self.loader.script_executor.execute(join_config.name, join_config.external_script).result)

        return concat.concatinate(*results).concatenate_result

    def run(self, *args, **kwargs) -> None:
        """
        Запуск процесса сбора данных, объединение их в единый сет,
        отправка данных подписчикам
        """
        preload_config = self.config_parser.parse_config(self.config['query']['preload'])
        piece_ids = list(self._execute_preload_step(preload_config))[0].result
        load_config = self._get_load_config(self.config_parser.parse_config(self.config['query']['load']), piece_ids)
        results = list(self._execute_load_step(load_config))
        join_config = self.config_parser.parse_config(self.config['script']['join'])
        result_joined = self._execute_join(join_config, results)
        self.outgoing_data.append(AsammMessage(data=result_joined))

        self.notify()


if __name__ == '__main__':
    r = Reader()
