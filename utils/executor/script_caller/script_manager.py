from importlib import util as importlib_util
from typing import Callable

from utils.executor.script_caller.external_script import ExternalScript


class ScriptManager:
    """
    Класс для управления внешними скриптами
    """

    @staticmethod
    def load(name: str, script_path: str):
        spec = importlib_util.spec_from_file_location(name, script_path)
        mod = importlib_util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return ExternalScript(module=mod, spec=spec)

    @staticmethod
    def reload(script: ExternalScript):
        if isinstance(script, ExternalScript):
            script.spec.loader.exec_module(script.module)
        raise TypeError()

    @staticmethod
    def get_func(script: ExternalScript, func_name: str) -> Callable:
        """
        Получит функции из загруженного модуля по имени
        :param script: объект загруженного скрипта
        :param func_name: имя вызываемой ф-ции
        :return: результат выполнения функции
        """
        if hasattr(script.module, func_name):
            return getattr(script.module, func_name)
        raise RuntimeError(f"Функция '{func_name}' в скрипте {script.module.__name__} не найдена.")
