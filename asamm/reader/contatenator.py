from typing import Callable

from utils.logger import LoggingMixin
from asamm import exception_handler
import pandas as pd


#@exception_handler
class Concatenator(LoggingMixin):
    concatenate_result = None

    def __init__(self, func_concat: Callable):
        self.func_concat = func_concat

    def concatinate(self, item1, item2, *args, **kwargs):
        if not item1:
            self.concatenate_result = item2
        else:
            self.concatenate_result = self.func_concat(item1, item2, *args, **kwargs)
        return self

    @classmethod
    def create_pandas_concatenator(cls):
        klass = cls(func_concat=pd.DataFrame.merge)
        return klass


# Example use
if __name__ == '__main__':
    d = {'col1': [1, 2], 'col2': ['a', 'b']}
    df1 = pd.DataFrame(data=d)

    d2 = {'col3': [3, 4], 'col2': ['a', 'b']}
    df2 = pd.DataFrame(data=d2)

    d3 = {'col30': [100, 400], 'col2': ['a', 'b']}
    df3 = pd.DataFrame(data=d3)

    print(df2)
    df2['col3'] = max(10, 30)

    print(df2)
    """
    concat = Concatenator.create_pandas_df_concatenator()
    concat \
        .concatinate(df1, df2, left_on='col2', right_on='col2', how='left') \
        .concatinate(concat.concatenate_result, df3, left_on='col2', right_on='col2', how='left')
    print(concat.concatenate_result)

    concat2 = Concatenator(func_concat=lambda a, b: a + b)
    concat2 \
        .concatinate(5, 5) \
        .concatinate(concat2.concatenate_result, 10)
    print(concat2.concatenate_result)
    """

