###################################################################
"""TEMPERATURES_Handler : Конвертор блока 'TEMPERATURES' в pandas DataFrame"""

__author__ = "Sergey Skachkov"
__version__ = "0.1"
__maintainer__ = "Alexander Titov"
__email__ = "titov_as@omk.ru"
__status__ = "Development"

###################################################################
import pandas as pd


def ExecuteFunc(df: pd.DataFrame) -> pd.DataFrame:
    """
    Выполняемая функция для преобразования json в pandas df
    :param df: DataFrame Pandas
    :return: DataFrame Pandas
    """
    df['TEMPERATURES_DEVICE_ID'] = df['TEMPERATURES_DEVICE_ID'].astype(str)

    df['TEMPERATURES(PIECE_ID+DEVICE_ID)'] = df['TEMPERATURES_PIECE_ID'].astype(str) + '+' + df[
        'TEMPERATURES_DEVICE_ID']
    df.drop_duplicates(subset=['TEMPERATURES(PIECE_ID+DEVICE_ID)'], inplace=True)
    df.drop(['TEMPERATURES(PIECE_ID+DEVICE_ID)'], axis=1, inplace=True)
    df = df.pivot(index='TEMPERATURES_PIECE_ID',
                  columns='TEMPERATURES_DEVICE_ID',
                  values=['TEMPERATURES_AVG_SOURCE',
                          'TEMPERATURES_MIN_SOURCE',
                          'TEMPERATURES_MAX_SOURCE',
                          'TEMPERATURES_STD_DEV_SOURCE',
                          'TEMPERATURES_BODY_AVG_VALUE',
                          'TEMPERATURES_BODY_MIN_VALUE',
                          'TEMPERATURES_BODY_MAX_VALUE',
                          'TEMPERATURES_HEAD_AVG_VALUE',
                          'TEMPERATURES_HEAD_MIN_VALUE',
                          'TEMPERATURES_HEAD_MAX_VALUE',
                          'TEMPERATURES_TAIL_AVG_VALUE',
                          'TEMPERATURES_TAIL_MIN_VALUE',
                          'TEMPERATURES_TAIL_MAX_VALUE'
                          ])

    return df


def main(arg) -> pd.DataFrame:
    return ExecuteFunc(arg)
