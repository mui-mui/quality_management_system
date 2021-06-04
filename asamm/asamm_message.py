from enum import Enum
from dataclasses import dataclass

@dataclass
class AsammMessage:
    COIL_ID: str
    PREDICTION_MODEL_RESULT: float
    WORK_MODEL_RESULT_DESCRIPTION: str

