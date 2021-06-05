from typing import List, Any

from dataclasses import dataclass
from asamm.model import AsammModel


@dataclass
class AsammMessage:
    """
    Класс для обмена данными между блоками системы АСАММ
    """
    models = list()
    raw_data: Any

    def add_model(self, model: AsammModel):
        self.models.append(model)

