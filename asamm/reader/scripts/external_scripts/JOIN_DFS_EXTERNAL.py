import pickle
import warnings

import pandas as pd


warnings.filterwarnings('ignore')








def main(arg) -> pd.DataFrame:




    df_coil_output = arg['HSM_CM_COIL_OUTPUT']
    df_average_ww = arg['HSM_AVERAGE_WW_COOLING']
    df_average_ic = arg['HSM_AVERAGE_IC_COOLING']
    df_cooling_rep = arg['HSM_COOLING_REPORT']
    df_rhf_lzone_info = arg['HSM_RHF_REP_DISC_LZONE_INFO']
    df_rhf_prod_info = arg['HSM_RHF_REP_DISC_PROD_INFO']
    df_hsm_sc_stat_rolling = arg['HSM_SC_STAT_ROLLING']
    df_temperatures = arg['HSM_TEMPERATURES']
    df_cm_furnance = arg['HSM_CM_FURNACE_HIST']
    df_chemistry = arg['MECH_TEST_CHEMISTRY']

    # будем присоединять все к главной таблице df_COIL_OUTPUT
    df_final = df_coil_output.merge(df_average_ww, left_on='COIL_OUTPUT_PIECE_ID',
                                    right_on='AVERAGE_WW_PIECE_ID', how='left')

    df_final = df_final.merge(df_average_ic, left_on='COIL_OUTPUT_PIECE_ID', right_on='AVERAGE_IC_PIECE_ID',
                              how='left')

    df_final = df_final.merge(df_cooling_rep, left_on='COIL_OUTPUT_PIECE_ID', right_on='COOLING_REP_PIECE_ID',
                              how='left')

    # таблица df_RHF_LZONE индексирована по ключам сбросим ключи для соединения
    # не понятно почему в зависящей таблице строк больше???(таблицы не очень хорошие печные)
    _df_rhf_lzone_info = df_rhf_lzone_info.reset_index()
    _df_rhf_prod_info = df_rhf_prod_info.merge(_df_rhf_lzone_info, left_on='RHF_PROD_INFO(BILL_ID+TF_ID)',
                                               right_on=[('RHF_LZONE_INFO(BILL_ID+TF_ID)', '')], how='left')
    df_final = df_final.merge(_df_rhf_prod_info, left_on='COIL_OUTPUT_PIECE_ID', right_on='RHF_PROD_INFO_PIECE_ID2',
                              how='left')

    # присоеденили еще df_stat_rolling
    # таблица df_stat_rolling индексирована по ключам сбросим ключи для соединения
    _df_hsm_sc_stat_rolling = df_hsm_sc_stat_rolling.reset_index()
    df_final = df_final.merge(_df_hsm_sc_stat_rolling, left_on='COIL_OUTPUT_PIECE_ID',
                              right_on=[('HSM_SC_STAT_ROLLING_PIECE_ID', '')],
                              how='left')

    # присоеденили еще df_TEMPERATURES
    # таблица df_TEMPERATURES индексирована по ключам сбросим ключи для соединения
    _df_temperatures = df_temperatures.reset_index()
    df_final = df_final.merge(_df_temperatures, left_on='COIL_OUTPUT_PIECE_ID',
                              right_on=[('TEMPERATURES_PIECE_ID', '')],
                              how='left')

    # присоеденили еще df_FURNACE_HIST
    # таблица df_CM_FURNACE_HIST индексирована по ключам сбросим ключи для соединения
    _df_cm_furnance = df_cm_furnance.reset_index()
    df_final = df_final.merge(_df_cm_furnance, left_on='COIL_OUTPUT_PIECE_ID', right_on=[('CM_FURNACE_PIECE_ID', '')],
                              how='left')

    df_final = df_final.merge(df_chemistry, left_on='COIL_OUTPUT_PIECE_ID', right_on='PIECE_ID', how='left')
    df_final = df_final.drop_duplicates(subset=['COIL_OUTPUT_COIL_ID'])

    return df_final

if __name__ == '__main__':

    with open(r"C:\work\asamm\reader\dump_join.pickle", "rb") as f:
        arg = pickle.load(f)
    main(arg)