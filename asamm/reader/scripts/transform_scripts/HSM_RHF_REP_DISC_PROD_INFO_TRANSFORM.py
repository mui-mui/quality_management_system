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
    df['RHF_PROD_INFO_BILL_ID'] = df['RHF_PROD_INFO_BILL_ID'].astype(str)
    df['RHF_PROD_INFO_TF_ID'] = df['RHF_PROD_INFO_TF_ID'].astype(str)
    df['RHF_PROD_INFO(BILL_ID+TF_ID)'] = df['RHF_PROD_INFO_BILL_ID'] + '+' + \
                                         df['RHF_PROD_INFO_TF_ID']
    df.drop_duplicates(subset=['RHF_PROD_INFO(BILL_ID+TF_ID)'], inplace=True)
    df.drop_duplicates(subset=['RHF_PROD_INFO_PIECE_ID2'], inplace=True)

    return df


def main(arg) -> pd.DataFrame:
    return ExecuteFunc(arg)

