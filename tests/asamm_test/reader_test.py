from asamm import AsammConfiguration
from utils.executor import SqlExecutor, ScriptExecutor
from utils.config_reader import read_config
from asamm.parse_config import SqlBlockConfigParser

import cx_Oracle
# TODO: Переделать!
cx_Oracle.init_oracle_client(r"C:\oracle\instantclient_18_3")




if __name__ == '__main__':
    sql_exec = SqlExecutor(AsammConfiguration.DATABASE_URI)
    script_exec = ScriptExecutor()

    sql_parser = SqlBlockConfigParser()


    #preload_conf = list(sql_parser.parse_config(read_config(AsammConfiguration.READER_CONFIG)['preload']))
    #preloader = Loader(sql_exec, script_exec)

    #gen = preloader.invoke(preload_conf)

    #for item in gen:
    piece_id = [1,2,3,4,5]

    for item in sql_parser.parse_config(read_config(AsammConfiguration.READER_CONFIG)['query']['preload']):
        script = script_exec.execute(item.name, item.before_query, "main").result
        item.query = script(item.query, piece_id)

