import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pathlib import Path

BASE_DIR = Path(__file__).parents[1]
OUTPUT_DIR = BASE_DIR / "output"
ANALYSIS_DIR = BASE_DIR / "analysis"

def plot_measures(
    df,
    filename: str,
    title: str,
    column_to_plot: str,
    y_label: str,
    as_bar: bool = False,
    category: str = None,
):
    """Produce time series plot from measures table.  One line is plotted for each sub
    category within the category column. Saves output in 'output' dir as jpeg file.
    Args:
        df: A measure table
        filename: Saved plot filename
        title: Plot title
        column_to_plot: Column name for y-axis values
        y_label: Label to use for y-axis
        as_bar: Boolean indicating if bar chart should be plotted instead of line chart. Only valid if no categories.
        category: Name of column indicating different categories
    """
    plt.figure(figsize=(15, 8))
    if category:
        for unique_category in sorted(df[category].unique()):

            # subset on category column and sort by date
            df_subset = df[df[category] == unique_category].sort_values("date")

            plt.plot(df_subset["date"], df_subset[column_to_plot])
    else:
        if as_bar:
            df.plot.bar("date", column_to_plot, legend=False)
        else:
            plt.plot(df["date"], df[column_to_plot])

    x_labels = sorted(df["date"].unique())

    plt.ylabel(y_label)
    plt.xlabel("Date")
    plt.xticks(x_labels, rotation="vertical")
    plt.title(title)
    plt.ylim(
        bottom=0,
        top=100
        if df[column_to_plot].isnull().values.all()
        else df[column_to_plot].max() * 1.05,
    )

    if category:
        plt.legend(
            sorted(df[category].unique()), bbox_to_anchor=(1.04, 1), loc="upper left"
        )

    plt.tight_layout()

    plt.savefig(OUTPUT_DIR / f"figures/{filename}.jpeg")
    plt.clf()

def calculate_rate(df, value_col, population_col, rate_per=1000, round_rate=False):
    """Calculates the number of events per 1,000 or passed rate_per variable of the population.
    This function operates on the given measure table in-place, adding
    a `rate` column.
    Args:
        df: A measure table.
        value_col: The name of the numerator column in the measure table.
        population_col: The name of the denominator column in the measure table.
        rate_per: Value to calculate rate per
        round: Bool indicating whether to round rate to 2dp.
    """
    if round_rate:
        rate = round(df[value_col] / (df[population_col] / rate_per), 2)

    else:
        rate = df[value_col] / (df[population_col] / rate_per)

    df["rate"] = num_per_thousand
