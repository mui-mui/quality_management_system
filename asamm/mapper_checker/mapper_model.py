from dataclasses import dataclass
from typing import Tuple

from asamm.parse_config import ConfigMapperBlock


@dataclass
class MapModel:
    data: Tuple
    configuration: ConfigMapperBlock
