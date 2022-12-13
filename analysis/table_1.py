import pandas as pd
import argparse
import glob
import pathlib
from analysis.utilities import OUTPUT_DIR
import numpy as np

def get_path(*args):
    return pathlib.Path(*args).resolve()

def match_paths(pattern):
    return [get_path(x) for x in sorted(glob.glob(pattern))]

def fill_missing_values(df, columns):
    """
    Fill missing values in the dataframe in provided columns with 'missing'.
    Args:
        df (pd.DataFrame): Dataframe to fill
        columns (list): List of columns to fill
    Returns:
        df (pd.DataFrame): Dataframe with missing values filled
    """    

    for column in columns:
        df[column] = df[column].fillna('missing')

    return df

def subset_outcome_of_interest(df, outcome):
    """
    Subset the dataframe to only include patients with the outcome of interest.
    Args:
        df (pd.DataFrame): Dataframe to subset
        outcome (str): Outcome of interest
    Returns:
        df (pd.DataFrame): Dataframe with the outcome of interest removed
        df_had_outcome (pd.DataFrame): Dataframe with only patients with the outcome of interest
    """
    df_had_outcome = df.loc[df[outcome]==1,:].reset_index(drop=True)
    df_had_outcome = df_had_outcome
    df = df.drop(outcome, axis=1)
    df_had_outcome = df_had_outcome.drop(outcome, axis=1)
    return df, df_had_outcome


def get_counts(df):
    """
    Get counts of patients in the dataframe for each column (demographic).
    Args:
        df (pd.DataFrame): Dataframe to get counts for
    Returns:
        counts (pd.DataFrame): Dataframe with counts for each demographic
    """
    
    df = df.drop("patient_id", axis=1)
    df_counts = df.apply(lambda x: x.value_counts()).T.stack()
    # set name to count
    df_counts.name = "count"
    return df_counts
   
def update_df(original_df, new_df, columns=[], on="patient_id"):
    """
    Update a dataframe with new data, overwriting old data where multiple values exist.
    Args:
        original_df (pd.DataFrame): Original dataframe
        new_df (pd.DataFrame): New dataframe
        columns (list): Columns to update
        on (str): Column to merge on
    Returns:
        pd.DataFrame: Updated dataframe
    """
    updated = original_df.merge(
        new_df, on=on, how="outer", suffixes=("_old", "_new"), indicator=True
    )

    for c in columns:
        updated[c] = np.nan
        updated.loc[updated["_merge"] == "left_only", c] = updated[f"{c}_old"]
        updated.loc[updated["_merge"] != "left_only", c] = updated[f"{c}_new"]
        updated = updated.drop([f"{c}_old", f"{c}_new"], axis=1)
    updated = updated.drop(["_merge"], axis=1)
    return updated



def create_table_1(paths, demographics, outcome):
    """
    Create a table 1 from a list of paths to csv files for the entire population and those with the outcome
    of interest. For each file in paths, the function will read in the demographics and outcome columns and
    merge them with the previous files. If a patient has multiple entries, the most recent entry will be used.
    Args:
        paths (list): List of paths to csv files
        demographics (list): List of demographics to include in the table
        outcome (str): Outcome of interest
    Returns:
        pd.DataFrame: Table 1
    """

    for i, path in enumerate(paths):
        if i ==0:
            # for the first file in the provided paths, we load it as the dataframe
            df = pd.read_csv(path, usecols=demographics + ["patient_id", outcome])
            
            #fill in missing values
            df = fill_missing_values(df, demographics)

            # create subset of patients with outcome of interest
            df, df_had_outcome = subset_outcome_of_interest(df, outcome)
            
        
        else:
            # if not the first file in the provided paths, we load it as the updated dataframe
            updated_df = pd.read_csv(path, usecols=demographics + ["patient_id", outcome])

            #fill in missing values
            updated_df = fill_missing_values(updated_df, demographics)

            # create subset of patients with outcome of interest
            updated_df, updated_df_had_outcome = subset_outcome_of_interest(updated_df, outcome)

            # update the original dataframe and with outcome dataframe
            df = update_df(df, updated_df, columns=demographics)
            df_had_outcome = update_df(df_had_outcome, updated_df_had_outcome, columns=demographics)
    
    df_counts = get_counts(df)
    df_counts_had_outcome = get_counts(df_had_outcome)

    return df_counts, df_counts_had_outcome

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--study_def_paths",
        dest="study_def_paths",
        required=True,
        type=match_paths,
        help="Glob pattern for matching input files",
    )

    parser.add_argument(
        "--demographics",
        dest="demographics",
        required=True,
        help="List of strings representing variables to include",
    )

    parser.add_argument(
        "--outcome",
        dest="outcome",
        required=True,
        help="String representing column title for outcome being looked at",
    )

    return parser.parse_args()


def main():
    args = parse_args()
    paths = args.study_def_paths
    demographics = args.demographics.split(",")
    outcome = args.outcome

    table_1, had_outcome = create_table_1(paths, demographics, outcome)
    table_1.to_csv(OUTPUT_DIR / "table_1.csv")
    had_outcome.to_csv(OUTPUT_DIR / "table_1_had_outcome.csv")

if __name__ == "__main__":
    main()