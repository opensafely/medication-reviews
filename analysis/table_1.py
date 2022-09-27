import pandas as pd
import argparse
import glob
import pathlib
from utilities import OUTPUT_DIR, update_df
from collections import Counter


def create_table_1(paths, demographics):

    for i, path in enumerate(paths):
        if i ==0:
            df = pd.read_csv(path, usecols=demographics + ["patient_id", "at_risk"])
            df_at_risk = df.loc[df["at_risk"]==1,:]
            df = df.drop("at_risk", axis=1)
            df_at_risk = df_at_risk.drop("at_risk", axis=1)
           
        
        else:
            updated_df = pd.read_csv(path, usecols=demographics + ["patient_id", "at_risk"])
            updated_df_at_risk = updated_df.loc[updated_df["at_risk"]==1,:]
            updated_df = updated_df.drop("at_risk", axis=1)
            updated_df_at_risk = updated_df_at_risk.drop("at_risk", axis=1)


            
            df = update_df(df, updated_df, columns=demographics)
            df_at_risk = update_df(df_at_risk, updated_df_at_risk, columns=demographics)
    
    df = df.drop("patient_id", axis=1)
    df_counts = df.apply(lambda x: x.value_counts()).T.stack()

    df_at_risk = df_at_risk.drop("patient_id", axis=1)
    df_counts_at_risk = df_at_risk.apply(lambda x: x.value_counts()).T.stack()

    return df_counts, df_counts_at_risk
   


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

    return parser.parse_args()


def main():
    args = parse_args()
    paths = args.study_def_paths
    demographics = args.demographics.split(",")

    table_1, at_risk = create_table_1(paths, demographics)
    table_1.to_csv(OUTPUT_DIR / "table_1.csv")
    at_risk.to_csv(OUTPUT_DIR / "table_1_at_risk.csv")


main()