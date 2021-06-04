import pandas as pd


def ExecuteFunc(df: pd.DataFrame) -> pd.DataFrame:
    """
    Выполняемая функция для преобразования json в pandas df
    :param df: DataFrame Pandas
    :return: DataFrame Pandas
    """
    df['RHF_LZONE_INFO_BILL_ID'] = df['RHF_LZONE_INFO_BILL_ID'].astype(str)
    df['RHF_LZONE_INFO_TF_ID'] = df['RHF_LZONE_INFO_TF_ID'].astype(str)
    df['RHF_LZONE_INFO_LZONE_ID'] = df['RHF_LZONE_INFO_LZONE_ID'].astype(str)
    df['RHF_LZONE_INFO(BILL_ID+TF_ID)'] = df['RHF_LZONE_INFO_BILL_ID'] + \
                                          '+' + df['RHF_LZONE_INFO_TF_ID']
    df['RHF_LZONE_INFO(BILL_ID+TF_ID+LZONE_ID)'] = df['RHF_LZONE_INFO_BILL_ID'] + \
                                                   '+' + df['RHF_LZONE_INFO_TF_ID'] + \
                                                   '+' + df['RHF_LZONE_INFO_LZONE_ID']
    df.drop_duplicates(subset=['RHF_LZONE_INFO(BILL_ID+TF_ID+LZONE_ID)'], inplace=True)
    df.drop(['RHF_LZONE_INFO_BILL_ID', 'RHF_LZONE_INFO_TF_ID', 'RHF_LZONE_INFO(BILL_ID+TF_ID+LZONE_ID)'],
            axis=1, inplace=True)

    df = df.pivot(index='RHF_LZONE_INFO(BILL_ID+TF_ID)', columns='RHF_LZONE_INFO_LZONE_ID',
                  values=['RHF_LZONE_INFO_AVE_TEMP',
                          'RHF_LZONE_INFO_BOT_TEMP',
                          'RHF_LZONE_INFO_CORE_TEMP',
                          'RHF_LZONE_INFO_TOP_TEMP',
                          'RHF_LZONE_INFO_HEAT_TIME',
                          'RHF_LZONE_INFO_ZONE_TEMP_MAX',
                          'RHF_LZONE_INFO_ZONE_TEMP_MIN',
                          'RHF_LZONE_INFO_ZONE_TEMP_AVG',
                          'RHF_LZONE_INFO_ZONE_SP_MAX',
                          'RHF_LZONE_INFO_ZONE_SP_MIN',
                          'RHF_LZONE_INFO_ZONE_SP_AVG',
                          'RHF_LZONE_INFO_ZONE_LMTD'
                          ])

    return df


def main(arg) -> pd.DataFrame:
    return ExecuteFunc(arg)
