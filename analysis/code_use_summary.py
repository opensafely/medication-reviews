import pandas as pd
import argparse
import glob
import pathlib
from utilities import OUTPUT_DIR
import numpy as np
import os

def create_codeuse_summary(paths):
    df_codeuse = pd.DataFrame(columns=['Code','Uses','Date'])
    codelistcolumns=[]
    CodeColumn=[]
    UsesColumn=[]
    DateColumn=[]
    for i, path in enumerate(paths):
        if i==0:
            filedate=get_date_from_filename(path)
            df = pd.read_csv(path)
            columnheaders=list(df)
            for column in columnheaders:
                if 'count_' in column:
                    codelistcolumns.append(column)
            for codecolumnname in codelistcolumns:
                codeonly=codecolumnname.replace('count_','')
                CodeColumn.append(codeonly)
                UsesColumn.append(df[codecolumnname].sum())
                DateColumn.append(filedate)
        else:
            filedate=get_date_from_filename(path)
            df = pd.read_csv(path) 
            for codecolumnname in codelistcolumns:
                codeonly=codecolumnname.replace('count_','')
                CodeColumn.append(codeonly)
                UsesColumn.append(df[codecolumnname].sum())
                DateColumn.append(filedate)
    dict = {'Code':CodeColumn,
            'Uses':UsesColumn,
            'Date':DateColumn
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
    df_codeuse=create_codeuse_summary(paths)
    df_codeuse.to_csv(OUTPUT_DIR / "codeuse.csv")


main()