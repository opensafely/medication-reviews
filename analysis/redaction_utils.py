import pandas as pd
import numpy as np


def round_column(column, base):
    return column.apply(lambda x: base * round(x / base) if pd.notnull(x) else x)

def drop_and_round(column, base=5, threshold=7):
    column[column <= threshold] = np.nan
    return round_column(column, base)


def redact_small_numbers(
    df, n, rounding_base, numerator, denominator, rate_column, date_column, standardised=True, standardised_column=None
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
        suppressed_column = column[column > n]

     
        # if suppressed values >0 ensure total suppressed count > threshold.
        # Also suppress if all values 0
        if (suppressed_count > 0) | (
            (suppressed_count == 0) & (len(suppressed_column) != len(column))
        ):


    
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
        if (standardised):
            df_subset.loc[
                (df_subset[numerator].isna()) | (df_subset[denominator].isna()), standardised_column
            ] = np.nan

        df_subset[rate_column] = df_subset[numerator] / df_subset[denominator]
        df_list.append(df_subset)

    return pd.concat(df_list, axis=0)


def codeuse_redact_small_numbers(
    df, n, rounding_base, column
):
    """
    Takes counts df as input and suppresses low numbers.  Sequentially redacts
    low numbers from column until count of redacted values >=n.
    Round counts to rounding_base.
    Rates corresponding to redacted values are also redacted.
    df: input df
    n: threshold for low number suppression
    rounding_base: rounding base to use
    column: column name for retraction
    """

    def suppress_column(column):
        suppressed_count = column[(column >0) & (column <= n)].sum()
     
        # if suppressed values >0 ensure total suppressed count > threshold.
        if (suppressed_count > 0):

            column[(column >0) & (column <= n)] = np.nan

            while suppressed_count <= n:
                suppressed_count += (column[column>0]).min()

                column[column[column>0].idxmin()] = np.nan
        column[column==np.nan] = 'REDACTED'
        return column

    df[column] = suppress_column(df[column])
    df[column] = round_column(df[column], base=rounding_base)

    df[column].fillna('REDACTED', inplace=True)

    return df