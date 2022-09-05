import pandas as pd
import argparse
import glob
import pathlib
from utilities import OUTPUT_DIR
from collections import Counter


def create_table(paths, demographics, outcome):

    demographics_dict = {d: {} for d in demographics}
    demographics_dict_total = {d: {} for d in demographics}

    demographics_dict_had_outcome = {d: {} for d in demographics}
    demographics_dict_had_outcome_total = {d: {} for d in demographics}
    for path in paths:
        df = pd.read_csv(path, usecols=demographics + ["patient_id", outcome])

        for i, row in df.iterrows():
            for d in demographics:
                if row[d]:
                    patient_id = row["patient_id"]
                    demographics_dict[d][patient_id] = row[d]
                    if row[outcome] == 1:
                        demographics_dict_had_outcome[d][patient_id] = row[d]
    for d in demographics:
        counts = dict(Counter([v for k, v in demographics_dict[d].items()]))
        demographics_dict_total[d] = counts

        counts_had_outcome = dict(Counter([v for k, v in demographics_dict_had_outcome[d].items()]))
        demographics_dict_had_outcome_total[d] = counts_had_outcome

    def reform_dict(dict):
        reformed_dict = {}
        reformed_dict["total"] = sum(dict[demographics[0]].values())
        for outerKey, innerDict in dict.items():
            for innerKey, values in innerDict.items():

                reformed_dict[(outerKey, innerKey)] = values
        return reformed_dict

    reformed_dict = reform_dict(demographics_dict_total)
    reformed_dict_had_outcome = reform_dict(demographics_dict_had_outcome_total)
    
    reformed_df = pd.DataFrame(reformed_dict, index=[0]).T
    reformed_df_had_outcome = pd.DataFrame(reformed_dict_had_outcome, index=[0]).T
    
    def join_summary_tables(reformed_df, reformed_df_had_outcome):
        reformed_df=reformed_df.rename(columns = {0: "Population"})
        reformed_df_had_outcome=reformed_df_had_outcome.rename(columns = {0: outcome})
        reformed_df_joined = pd.merge(reformed_df, reformed_df_had_outcome,  left_index=True, right_index=True)
        reformed_df_joined["%"] = reformed_df_joined[outcome]/reformed_df_joined["Population"]
        return reformed_df_joined

    reformed_df_joined = join_summary_tables(reformed_df, reformed_df_had_outcome)

    return (
        reformed_df,
        reformed_df_had_outcome,
        reformed_df_joined
    )


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

    table, had_outcome, joined_table = create_table(paths, demographics, outcome)
    table.to_csv(OUTPUT_DIR / "table.csv")
    had_outcome.to_csv(OUTPUT_DIR / "table_had_outcome.csv")
    joined_table.to_csv(OUTPUT_DIR / "table_joined.csv")


main()