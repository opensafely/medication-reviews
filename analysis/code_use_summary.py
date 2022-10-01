import pandas as pd
import argparse
import glob
import pathlib
from utilities import OUTPUT_DIR
import numpy as np
from codelists import *

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

    return parser.parse_args()

def main():
    args = parse_args()
    paths = args.study_def_paths
    variables = {}
    for code in code_list:
        variables.update(make_variable(code))

    #demographics = args.demographics.split(",")
    #outcome = args.outcome

    #table_1, had_outcome = create_table_1(paths, demographics, outcome)
    #table_1.to_csv(OUTPUT_DIR / "table_1.csv")
    #had_outcome.to_csv(OUTPUT_DIR / "table_1_had_outcome.csv")


main()