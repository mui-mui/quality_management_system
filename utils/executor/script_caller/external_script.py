from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ExternalScript:
    module: Any
    spec: Any
