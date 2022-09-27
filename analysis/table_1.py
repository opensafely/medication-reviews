import pandas as pd
import argparse
import glob
import pathlib
from utilities import OUTPUT_DIR, update_df
import numpy as np


def create_table_1(paths, demographics, outcome):

    for i, path in enumerate(paths):
        if i ==0:
            df = pd.read_csv(path, usecols=demographics + ["patient_id", outcome])
            df_had_outcome = df.loc[df[outcome]==1,:]
            df = df.drop(outcome, axis=1)
            df_had_outcome = df_had_outcome.drop(outcome, axis=1)
           
        
        else:
            updated_df = pd.read_csv(path, usecols=demographics + ["patient_id", outcome])
            updated_df_had_outcome = updated_df.loc[updated_df[outcome]==1,:]
            updated_df = updated_df.drop(outcome, axis=1)
            updated_df_had_outcome = updated_df_had_outcome.drop(outcome, axis=1)


            
            df = update_df(df, updated_df, columns=demographics)
            df_had_outcome = update_df(df_had_outcome, updated_df_had_outcome, columns=demographics)
    
    df = df.drop("patient_id", axis=1)
    df_counts = df.apply(lambda x: x.value_counts()).T.stack()

    df_had_outcome = df_had_outcome.drop("patient_id", axis=1)
    df_counts_had_outcome = df_had_outcome.apply(lambda x: x.value_counts()).T.stack()

    return df_counts, df_counts_had_outcome
   
def update_df(original_df, new_df, columns=[], on="patient_id"):
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

def get_path(*args):
    return pathlib.Path(*args).resolve()


def match_paths(pattern):
    return [get_path(x) for x in sorted(glob.glob(pattern))]


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


main()