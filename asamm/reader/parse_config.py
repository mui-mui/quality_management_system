from abc import ABC, abstractmethod
from collections import namedtuple
from dataclasses import dataclass


@dataclass
class ConfigScriptBlock:
    name: str
    external_script: str


@dataclass
class ConfigSqlBlock:
    name: str
    query: str
    setup_query: str
    transform_script: str


class IConfigParser(ABC):

    def parse_config(self, data):
        # conf_obj = read_config(conf_path)
        # block = conf_obj[type_block][block_name]

        if not isinstance(data, list):
            data = [data]
        for item in data:
            yield self.create_block(item)

    @abstractmethod
    def create_block(self, block_item):
        pass


class SqlBlockConfigParser(IConfigParser):
    def create_block(self, block_item):
        return ConfigSqlBlock(name=block_item['name'],
                              query=block_item['query'],
                              setup_query=block_item['before_query'],
                              transform_script=block_item['after_query'])


class ScriptBlockConfigParser(IConfigParser):
    def create_block(self, block_item):
        return ConfigScriptBlock(name=block_item['name'],
                                 external_script=block_item['script_path'])
