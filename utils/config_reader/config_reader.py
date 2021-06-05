import pathlib

import yaml


def read_config(config_path):
    with open(config_path, encoding="UTF8") as f:
        config = yaml.safe_load(f)
    return config
