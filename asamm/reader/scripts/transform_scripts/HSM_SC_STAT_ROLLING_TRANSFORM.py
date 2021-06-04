###################################################################
"""HSM_SC_STAT_ROLLING_Handler : Конвертация блока 'HSM_SC_STAT_ROLLING' в pandas DataFrame"""

__author__ = "Sergey Skachkov"
__version__ = "0.1"
__maintainer__ = "Alexander Titov"
__email__ = "titov_as@omk.ru"
__status__ = "Development"

###################################################################
import base64
import pickle

import pandas as pd
import sys


def ExecuteFunc(df: pd.DataFrame) -> pd.DataFrame:
    """
    Выполняемая функция для преобразования json в pandas df
    :param df: DataFrame Pandas
    :return: DataFrame Pandas
    """
    df['HSM_SC_STAT_ROLLING(PIECE_ID+STAND_ID+SECTION+STAT_IDX)'] = \
        df['HSM_SC_STAT_ROLLING_PIECE_ID'].astype(str) + '+' + df['HSM_SC_STAT_ROLLING_STAND_ID'].astype(
            str) + \
        '+' + df['HSM_SC_STAT_ROLLING_SECTION'].astype(str) + '+' + df['HSM_SC_STAT_ROLLING_STAT_IDX'].astype(
            str)

    df['HSM_SC_STAT_ROLLING(STAND_ID+SECTION+STAT_IDX)'] = \
        df['HSM_SC_STAT_ROLLING_STAND_ID'] + '+' + df['HSM_SC_STAT_ROLLING_SECTION'] + \
        '+' + df['HSM_SC_STAT_ROLLING_STAT_IDX']

    df.drop(['HSM_SC_STAT_ROLLING_STAND_ID', 'HSM_SC_STAT_ROLLING_SECTION', 'HSM_SC_STAT_ROLLING_STAT_IDX'],
            axis=1, inplace=True)
    df.drop_duplicates(subset=['HSM_SC_STAT_ROLLING(PIECE_ID+STAND_ID+SECTION+STAT_IDX)'], inplace=True)
    df.drop(['HSM_SC_STAT_ROLLING(PIECE_ID+STAND_ID+SECTION+STAT_IDX)'], axis=1, inplace=True)
    df = df.pivot(
        index='HSM_SC_STAT_ROLLING_PIECE_ID',
        columns='HSM_SC_STAT_ROLLING(STAND_ID+SECTION+STAT_IDX)',
        values=['HSM_SC_STAT_ROLLING_EXIT_THICK', 'HSM_SC_STAT_ROLLING_FORCE', 'HSM_SC_STAT_ROLLING_TORQUE',
                'HSM_SC_STAT_ROLLING_CURRENT', 'HSM_SC_STAT_ROLLING_SPEED'])

    return df


def main(arg):
    return ExecuteFunc(arg)
