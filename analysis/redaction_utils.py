import pandas as pd
import numpy as np


def round_column(column, base):
    return column.apply(lambda x: base * round(x / base) if pd.notnull(x) else x)

def drop_and_round(column, base=5, threshold=7):
    column[column <= threshold] = np.nan
    return round_column(column, base)


def redact_small_numbers(
    df, n, rounding_base, numerator, denominator, rate_column, date_column
):
    """
    Takes counts df as input and suppresses low numbers.  Sequentially redacts
    low numbers from numerator and denominator until count of redacted values >=n.
    Round counts to rounding_base.
    Rates corresponding to redacted values are also redacted.
    df: input df
    n: threshold for low number suppression
    rounding_base: rounding base to use
    numerator: numerator column to be redacted
    denominator: denominator column to be redacted
    """

    def suppress_column(column):
        suppressed_count = column[column <= n].sum()

        # if 0 dont need to suppress anything
        if suppressed_count == 0:
            pass

        else:
            column[column <= n] = np.nan

            while suppressed_count <= n:
                suppressed_count += column.min()

                column[column.idxmin()] = np.nan
        return column

    df_list = []

    dates = df[date_column].unique()

    for d in dates:
        df_subset = df.loc[df[date_column] == d, :]

        for column in [numerator, denominator]:
            df_subset[column] = suppress_column(df_subset[column])
            df_subset[column] = round_column(df_subset[column], base=rounding_base)

        df_subset.loc[
            (df_subset[numerator].isna()) | (df_subset[denominator].isna()), rate_column
        ] = np.nan
        df_subset[rate_column] = df_subset[numerator] / df_subset[denominator]
        df_list.append(df_subset)

    return pd.concat(df_list, axis=0)