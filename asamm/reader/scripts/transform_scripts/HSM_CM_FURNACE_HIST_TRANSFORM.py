###################################################################
"""CM-FURNANCE_Handler.py : Конвертор блока 'CM_FURNANCE' в pandas DataFrame"""

__author__ = "Sergey Skachkov"
__version__ = "0.1"
__maintainer__ = "Alexander Titov"
__email__ = "titov_as@omk.ru"
__status__ = "Development"

###################################################################
import base64

import pandas as pd
import sys
import pickle


def ExecuteFunc(df: pd.DataFrame) -> pd.DataFrame:
    """
    Выполняемая функция для преобразования json в pandas df
    :param df: DataFrame Pandas
    :return: DataFrame Pandas
    """
    df_furnance_1 = df.copy()
    df_furnance_1['CM_FURNACE(PIECE_ID+FURNACE)'] = df['CM_FURNACE_PIECE_ID'].astype(str) + '+' + df[
        'CM_FURNACE_FURNACE']
    df_furnance_1.drop_duplicates(subset=['CM_FURNACE(PIECE_ID+FURNACE)'], inplace=True)
    df_furnance_1.drop(['CM_FURNACE(PIECE_ID+FURNACE)'], axis=1, inplace=True)
    df_furnance = df_furnance_1.pivot(
        index='CM_FURNACE_PIECE_ID',
        columns='CM_FURNACE_FURNACE',
        values=['CM_FURNACE_TIME_IN_FRN', 'CM_FURNACE_EXPECTED_TEMP', 'CM_FURNACE_DISCHARGE_TEMP'])

    return df_furnance


def main(arg) -> pd.DataFrame:
    return ExecuteFunc(arg)

