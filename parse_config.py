from abc import ABC, abstractmethod
from collections import namedtuple
from dataclasses import dataclass
from typing import List, Any, Callable
from ast import literal_eval as make_tuple

Inspection = namedtuple("Inspection", ['r2', 'sko', 'val'])
SteelGrade = namedtuple("SteelGrade", ['grade', 'inspection'])
Encoder = namedtuple("Encoder", ['continuous', 'fast', 'late', 'intensive', 'non_type', 'intensive_short'])
Property = namedtuple("Property", ['property_type', 'test_type', 'direction'])


@dataclass
class ConfigModelBlock:
    steel_grade: 'List[SteelGrade]'
    columns: Any
    tensor_file: str
    scaler_file: str
    property: 'Property'
    encoder: 'Encoder'


@dataclass
class ConfigMapperBlock:
    id: str
    name: str
    model_file: str
    settings_file: str
    model_config: ConfigModelBlock = None
    model_func: Callable = None


@dataclass
class ConfigScriptBlock:
    id: str
    name: str
    external_script: str


@dataclass
class ConfigSqlBlock:
    id: str
    name: str
    query: str
    setup_query: str
    transform_script: str


class IConfigParser(ABC):

    def parse_config(self, data):
        # conf_obj = read_config(conf_path)
        # block = conf_obj[type_block][block_name]

        if not isinstance(data, list):
            yield data
        else:
            for item in data:
                yield self.create_block(item)

    @abstractmethod
    def create_block(self, block_item):
        pass


class SqlBlockConfigParser(IConfigParser):
    def create_block(self, block_item):
        return ConfigSqlBlock(id=block_item['id'],
                              name=block_item['name'],
                              query=block_item['query'],
                              setup_query=block_item['setup_query'],
                              transform_script=block_item['transform_script'])


class ScriptBlockConfigParser(IConfigParser):
    def create_block(self, block_item):
        return ConfigScriptBlock(id=block_item['id'],
                                 name=block_item['name'],
                                 external_script=block_item['external_script'])


class MapperBlockConfigParser(IConfigParser):
    def create_block(self, block_item):
        return ConfigMapperBlock(id=block_item['id'],
                                 name=block_item['name'],
                                 model_file=block_item['model_file'],
                                 settings_file=block_item['settings_file'])


class ModelConfigParser(IConfigParser):
    def create_block(self, block_item):
        steel_grade_list = []
        for item in block_item["steel_grade"]:
            steel_grade_list.append(SteelGrade(
                grade=item["grade"],
                inspection=Inspection(
                    r2=item["inspection"]["r2"],
                    sko=item["inspection"]["sko"],
                    val=item["inspection"]["val"]
                )
            ))

        return ConfigModelBlock(
            steel_grade=steel_grade_list,
            columns=[make_tuple(item) if item.startswith("(") else item for item in block_item["columns"]],
            tensor_file=block_item["tensor_file"],
            scaler_file=block_item["scaler_file"],
            property=Property(property_type=block_item["property"]["property_type"],
                              test_type=block_item["property"]["test_type"],
                              direction=block_item["property"]["direction"]),
            encoder=Encoder(continuous=block_item["encoder"]["CONTINUOUS"],
                            fast=block_item["encoder"]["FAST"],
                            late=block_item["encoder"]["LATE"],
                            intensive=block_item["encoder"]["INTENSIVE"],
                            non_type=block_item["encoder"]["---"],
                            intensive_short=block_item["encoder"]["INTENSIVE_SHORT"])
        )
