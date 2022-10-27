import pandas as pd
import argparse
import glob
import pathlib
from utilities import OUTPUT_DIR, CODELIST_DIR, plot_measures
import numpy as np
import os
from pathlib import Path

if not (OUTPUT_DIR / "figures").exists():
    Path.mkdir(OUTPUT_DIR / "figures")

def get_column_codes(codelist_file):
    df = pd.read_csv(CODELIST_DIR / codelist_file)
    df['code'] = df['code'].astype(str)
    listofcodes=df['code'].values.tolist()
    return listofcodes

def get_terms_for_codes(codelist_file):
    df = pd.read_csv(CODELIST_DIR / codelist_file)
    df['code'] = df['code'].astype(str)
    #Create column with term and code
    df['termcode']=df['term']+' ('+df['code']+')'
    return df

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
    filename=filenamesplit[0]
    filename=filename.replace('input_', '')
    filename=filename.replace('allmedrev_', '')
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
    parser.add_argument(
        "--codelistfile",
        dest="codelistfile",
        required=True,
        help="Filename of codelist",
    )
    parser.add_argument(
        "--outputfile",
        dest="outputfile",
        required=True,
        help="Output filename",
    )

    return parser.parse_args()

def main():
    args = parse_args()
    paths = args.study_def_paths
    codelist_file = args.codelistfile
    outputfile = args.outputfile

    #Get codes from codelist to use to identify columns of interest
    code_columns = get_column_codes(codelist_file)

    #Get term names from codelist to use to translate to understandable terms
    terms_lookup=get_terms_for_codes(codelist_file)

    df_codeuse=create_codeuse_summary(paths, code_columns)

    #Add term names onto table
    df_codeuse = pd.merge(df_codeuse, terms_lookup, how='left', left_on = 'code', right_on = 'code')

    #Reorder columns
    df_codeuse=df_codeuse.reindex(columns=['code','term','termcode','uses','date'])
    
    df_codeuse.to_csv(OUTPUT_DIR / f"{outputfile}.csv", index=False)

main()