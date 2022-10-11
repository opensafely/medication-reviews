import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from cohortextractor import patients, codelist

from pathlib import Path

BASE_DIR = Path(__file__).parents[1]
OUTPUT_DIR = BASE_DIR / "output"
ANALYSIS_DIR = BASE_DIR / "analysis"
CODELIST_DIR = BASE_DIR / "codelists"

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
    mask = np.isfinite(df[column_to_plot])

    if category:
        for unique_category in sorted(df[category].unique()):

            # subset on category column and sort by date
            df_subset = df[df[category] == unique_category].sort_values("date")

            plt.plot(df_subset["date"][mask], df_subset[column_to_plot][mask], marker='o')
    else:
        if as_bar:
            df.plot.bar("date", column_to_plot, legend=False)
        else:
            plt.plot(df["date"][mask], df[column_to_plot][mask], marker='o')

    x_labels = sorted(df["date"].unique())

    plt.ylabel(y_label)
    plt.xlabel("Date")
    plt.xticks(x_labels, rotation="vertical")

    #Format dates for x-axis
    dtFmt = mdates.DateFormatter('%B %Y') # define the date formatting
    plt.gca().xaxis.set_major_formatter(dtFmt) # apply the format to the desired axis 


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
    plt.vlines(
        x=[pd.to_datetime("2020-03-23")],
        ymin=0,
        ymax=df[column_to_plot].max() * 1.05,
        colors="orange",
        ls="--",
        label="First National Lockdown",
    )
    
    plt.vlines(
        x=[pd.to_datetime("2020-11-05")],
        ymin=0,
        ymax=df[column_to_plot].max() * 1.05,
        colors="orange",
        ls="--",
        label="Second National Lockdown",
    )
    
    plt.vlines(
        x=[pd.to_datetime("2021-01-04")],
        ymin=0,
        ymax=df[column_to_plot].max() * 1.05, 
        colors="orange",
        ls="--",
        label="Third National Lockdown",
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
    df["rate"] = rate

def binary_care_home_status(
    df,
    numerator_column: str,
    denominator_column: str,
):
    """Converts various care home types into binary value..
    Args:
        df: A measure table
        numerator_column: Column heading to use as numerator
        denominator_column: Column heading to use as denominator
    """ 
    df = df.replace({'CareHome': 1, 'CareOrNursingHome': 1, 'NursingHome':1, 'PrivateHome':0, 'missing': 0})
    grouped_df = df.groupby(["care_home_type", "date"], as_index=False)[[numerator_column, denominator_column]].sum()
    grouped_df['value'] = grouped_df[numerator_column]/grouped_df[denominator_column]
    return grouped_df

def convert_binary(df, binary_column, positive, negative):
    """Converts a column with binary variable codes as 0 and 1 to understandable strings.
    Args:
        df: dataframe with binary column
        binary_column: column name of binary variable
        positive: string to encode 1 as
        negative: string to encode 0 as
    Returns:
        Input dataframe with converted binary column
    """
    replace_dict = {0: negative, 1: positive}
    df[binary_column] = df[binary_column].replace(replace_dict)
    return df

def loop_over_codes(code_list):
    def make_variable(code):
        return {
            f"count_{code}": (
                patients.with_these_clinical_events(
                    codelist([code], system="snomed"),
                    between =["first_day_of_month(index_date)", "last_day_of_month(index_date)"],
                    returning="number_of_matches_in_period",
                    return_expectations={
                         "incidence": 0.1,
                         "int": {"distribution": "normal", "mean": 3, "stddev": 1},
                    },
                )
            )
        }

    variables = {}
    for code in code_list:
        variables.update(make_variable(code))
    return variables
