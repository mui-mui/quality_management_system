from collections import deque, namedtuple
from typing import Deque, List, Iterable

import pandas

from asamm import AsammConfiguration
from asamm.asamm_message import AsammMessage
from asamm.asamm_node import ISystemNode, IProducer
from asamm.mapper_checker.mapper_model import MapModel
from asamm.reader.loader import Loader
from asamm.parse_config import MapperBlockConfigParser, ModelConfigParser, ConfigMapperBlock
from utils.config_reader import read_config


class Mapper(ISystemNode):
    """
    Класс назначения моделей из конфигурационного файла
    для входящих данных
    """
    outgoing_data: Deque[AsammMessage] = deque()
    config = read_config(AsammConfiguration.MAPPER_CONFIG)

    def __init__(self, loader: Loader):
        self.mapper_config_parser = MapperBlockConfigParser()
        self.model_config_parser = ModelConfigParser()
        self.loader = loader

    @property
    def get_messages_queue(self) -> Deque:
        return self.outgoing_data

    def notify(self):
        super().notify()

    def update(self, producer: IProducer):
        """
        Запуск маппинга входящих данных с конфигурациями моделей в системе
        """
        while True:
            try:
                message: AsammMessage = producer.get_messages_queue.pop()
                for item in self._create_map_configuration(message.raw_data):
                    self.outgoing_data.append(AsammMessage(raw_data=item))
                    self.notify()  # оповещение по факту отправки каждого сообщения
            except IndexError:
                break

    def run(self, *args, **kwargs):
        raise NotImplementedError()

    def _prepare_config(self) -> List[ConfigMapperBlock]:
        """
        Читает конфигурации моделей по путям, указанными в конфиграции маппера,
        присоединяет ее в виде объектов к конф. маппера
        """
        MODEL_FUNC_NAME = "NeuralModel"

        mapper_config: List[ConfigMapperBlock] = list(self.mapper_config_parser.parse_config(self.config))
        for item in mapper_config:
            item.model_func = self.loader.script_executor.execute(item.id, item.name, item.model_file,
                                                                  MODEL_FUNC_NAME).result
            item.model_config = list(self.model_config_parser.parse_config(read_config(item.settings_file)))[0]

        return mapper_config

    def _create_map_configuration(self, data: pandas.DataFrame) -> Iterable[MapModel]:
        """
        Маппинг конфигурации с входящими данными.
        Маппинг проводится по наличию марки стали в конфигурации модели
        """
        STEEL_GRADE_FIELD = "coil_output_steel_grade"  # "COIL_OUTPUT_STEEL_GRADE"

        update_mapper_config = self._prepare_config()

        for row in (data.loc[i:i, :] for i in range(0, len(data), 1)):
            steel_grade = row[STEEL_GRADE_FIELD].values[0]
            for mapper_config_block in filter(
                    lambda item: steel_grade in set([st.grade for st in item.model_config.steel_grade]),
                    update_mapper_config):
                yield MapModel(data=row, configuration=mapper_config_block)
