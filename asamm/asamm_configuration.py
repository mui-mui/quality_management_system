import os
import pathlib

from system_config import SystemConfig

BASE_DIR = pathlib.Path(__file__).parent


class AsammConfiguration(SystemConfig):
    READER_CONFIG = BASE_DIR / 'reader' / 'reader_config.yaml'
    MAPPER_CONFIG = BASE_DIR / 'mapper' / 'mapper_config.yaml'
    DATABASE_URI = os.environ['ASAMM_DATABASE_URI']
