import pandas as pd
import argparse
from pathlib import Path
import re

def match_input_files(file: str) -> bool:
    """Checks if file name has format outputted by cohort extractor"""
    pattern = r"^input_report_20\d\d-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[01])\.csv.gz"
    return True if re.match(pattern, file) else False


def get_date_input_file(file: str) -> str:
    """Gets the date in format YYYY-MM-DD from input file name string"""
    # check format
    if not match_input_files(file):
        raise Exception("Not valid input file format")

    else:
        date = re.search(r"input_report_(.*).csv.gz", file)
        return date.group(1)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--breakdowns', type=str, required=True)
    parser.add_argument('--input_dir', type=str, required=True)
    parser.add_argument('--measure', type=str, required=True)
    return parser.parse_args()

def main():
    args = parse_args()
    
    if not args.breakdowns == "":
       
        breakdowns = [x for x in args.breakdowns.split(",")]
    else:
        breakdowns = []
    
    breakdowns.extend(["practice","event_1_code", "event_2_code"])
    data = {"total": []}
    for b in breakdowns:
        data[b] = []

    print(breakdowns)

    for file in Path(args.input_dir).iterdir():
      
        if match_input_files(file.name):
            date = get_date_input_file(file.name)
            
            df = pd.read_csv(file)
            print(df.columns)
            df["date"] = date
            count = df.loc[:,"event_measure"].sum()
            population = df.loc[:,"event_measure"].count()
            value = count/population
            row_dict ={
                "date": pd.Series([date]),
                "event_measure": pd.Series([count]),
                "population": pd.Series([population]),
                "value": pd.Series([value])
            }

            # make df from row_dict

            df_row = pd.DataFrame(row_dict)
            

            
            data["total"].append(df_row)

            for breakdown in breakdowns:
                counts = df.groupby(by=[breakdown])[["event_measure"]].sum()
                counts["population"] = df.groupby(by=[breakdown])[["event_measure"]].count()
                counts["value"] = counts["event_measure"] / counts["population"]
                counts=counts.reset_index()
                counts["date"] = date
                data[breakdown].append(counts)

    df = pd.concat(data["total"])
    df.to_csv(f"{args.input_dir}/measure_total_rate.csv", index=False)
    for breakdown in breakdowns:
        df = pd.concat(data[breakdown])
        df.to_csv(f"{args.input_dir}/measure_{breakdown}_rate.csv", index=False)
  
   

if __name__ == "__main__":
    main()