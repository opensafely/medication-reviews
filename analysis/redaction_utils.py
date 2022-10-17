import pandas as pd
import numpy as np


def round_column(column, base):
    return column.apply(lambda x: base * round(x / base) if pd.notnull(x) else x)

def drop_and_round(column, base=5, threshold=7):
    column[column <= threshold] = np.nan
    return round_column(column, base)
