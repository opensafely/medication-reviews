import pandas as pd
import argparse
import glob
import pathlib
from utilities import OUTPUT_DIR, CODELIST_DIR, plot_measures
import numpy as np
import os
from pathlib import Path
from codelists import med_review_codes

if not (OUTPUT_DIR / "figures").exists():
    Path.mkdir(OUTPUT_DIR / "figures")

def get_column_codes(code_list):
    variables = []
    for code in code_list:
        variables.append(code)
    return variables

def get_terms_for_codes(codelist_file):
    df = pd.read_csv(CODELIST_DIR / codelist_file)
    return df


"codelists/user-chriswood-medication-review.csv"

def create_codeuse_summary(paths, code_columns):
    CodeColumn=[]
    UsesColumn=[]
    DateColumn=[]
    for path in paths:
        filedate=get_date_from_filename(path)
        df = pd.read_csv(path) 
        for codecolumnname in code_columns:
            CodeColumn.append(codecolumnname)
            UsesColumn.append(df[f'count_{codecolumnname}'].sum())
            DateColumn.append(filedate)
    dict = {'code':CodeColumn,
            'uses':UsesColumn,
            'date':DateColumn
            }
  
    df_codeuse = pd.DataFrame(dict)
    return df_codeuse                        



def get_date_from_filename(path):
    pathsplit=os.path.normpath(path).split(os.path.sep)
    filenamesplit=pathsplit[-1].split('.')
    filename=filenamesplit[0].replace('input_', '')
    filedatesplit=filename.split('-')
    filedate=f'{filedatesplit[2]}/{filedatesplit[1]}/{filedatesplit[0]}'
    return filedate

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
    code_columns = get_column_codes(med_review_codes)
    df_codeuse=create_codeuse_summary(paths, code_columns)
    df_codeuse['code']=df_codeuse['code'].astype(int)
    terms_lookup=get_terms_for_codes()
    df_codeuse = pd.merge(df_codeuse, terms_lookup, how='left', left_on = 'code', right_on = 'code')
    df_codeuse=df_codeuse.reindex(columns=['code','term','uses','date'])
    df_codeuse.to_csv(OUTPUT_DIR / "codeuse.csv", index=False)
    df_codeuse['date']= pd.to_datetime(df_codeuse['date'])
    plot_measures(df_codeuse, 'codeuse', '', 'uses', 'Uses of code',  category='term')


main()