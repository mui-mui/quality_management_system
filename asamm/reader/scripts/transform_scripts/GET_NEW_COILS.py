from typing import List, Tuple
import pandas
from collections import namedtuple


def main(df: pandas.DataFrame):
    return {item[0]: item[1] for item in zip(df["piece_id"].values.tolist(), df["coil_id"].values.tolist())}
