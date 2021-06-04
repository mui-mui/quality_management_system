from utils.executor.iblockcaller import IBlockCaller
from utils.executor.script_caller.script_manager import ScriptManager
from utils.handlers import AllExceptionsHandled
from utils.executor.call_result import call_result


class ScriptBlockCaller(IBlockCaller):
    """
    Исполнитель блока типа 'SCRIPT' из конфигурации
    """

    def call(self, id_, name: str, external_script: str, func_name: str):
        """
        Запуск внешнего скрипта  
        """
        self.info(f"Выполнение внешнего скрипта '{name}'...")
        script_obj = ScriptManager.load(name, external_script)
        func = ScriptManager.get_func(script_obj, func_name)
        return call_result(
            id=id_,
            name=name,
            result=func,
            error=f"Скрипт {name} вернул null" if not func else None)
