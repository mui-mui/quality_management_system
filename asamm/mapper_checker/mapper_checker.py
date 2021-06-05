from typing import Deque
from collections import deque

import pandas

from asamm.asamm_message import AsammMessage
from utils.handlers import coroutine
from utils.handlers import AllExceptionsHandled
from asamm.asamm_node import ISystemNode, IProducer
from asamm.ichecker import IChecker


@AllExceptionsHandled(logged_call=True)
class MapperChecker(ISystemNode, IChecker):
    """
    Класс содержит комплекс проверок перед
    блоком 'Mapper'
    """
    outgoing_data = deque()
    _chek_result = None  # запись результата текущей проверки

    @property
    def get_messages_queue(self) -> Deque:
        return self.outgoing_data

    def notify(self):
        super().notify()

    def update(self, producer: IProducer):
        """
        Запуск цепочки проверок перед блоком маппера
        Отправка данных  подписчикам
        """
        while True:
            try:
                message: AsammMessage = producer.get_messages_queue.pop()
                self.run_all_checks(message.raw_data)  # запуск цепочки проверок
                self.outgoing_data.append(self._chek_result)  # запись результа цепочки в очередь
                self.notify()
            except IndexError:
                break

    def run_all_checks(self, data_for_checks):
        super().run_all_checks(data_for_checks)

    @coroutine
    def check_chemistry_data_availability(self, target=None):
        """
        Проверка наличия данных по химии для поступивших COIL ID
        """
        FIELD_NAME_FOR_CHECK = "CHEMISTRY_CR"

        while True:
            data: pandas.DataFrame = yield
            rows_chemistry_null = pandas.isnull(data[FIELD_NAME_FOR_CHECK])
            rows_chemistry_not_null = pandas.notnull(data[FIELD_NAME_FOR_CHECK])
            if coils := data[rows_chemistry_null].values.tolist():
                self.warning(self.warning(
                    f"Внимание! Обработка для следующих COIL ID будет приостановлена: "
                    f"отсутствуют данные по химии!\n COIL_ID: {', '.join(coils)}"))

            self._chek_result = data[rows_chemistry_not_null]
            if target:
                target.send(self._chek_result)

    def run(self, *args, **kwargs):
        raise NotImplementedError()

    """
    @coroutine
    def check2(self, target=None):
        
        Проверка чек1
        
        while True:
            s = yield
            print(f"Check2 Get {s}")
            if target:
                target.send(s * s)
    """
