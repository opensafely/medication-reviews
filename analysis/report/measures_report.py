import pandas as pd
import argparse
from pathlib import Path
from report_utils import match_input_files, get_date_input_file



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

   

    for file in Path(args.input_dir).iterdir():
      
        if match_input_files(file.name):
            date = get_date_input_file(file.name)
            
            df = pd.read_csv(file)

            if "sex" in breakdowns:
                df = df.loc[df["sex"].isin(["M", "F"]),:]
            
            df["date"] = date
            count = df.loc[:,"event_measure"].sum()
            population = df.loc[:,"event_measure"].count()
            value = (count/population)*1000
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
                counts["value"] = (counts["event_measure"] / counts["population"])*1000
                counts=counts.reset_index()
                counts["date"] = date
                data[breakdown].append(counts)

    df = pd.concat(data["total"])
    # sort by date
    df = df.sort_values(by=["date"])
    df.to_csv(f"{args.input_dir}/measure_total_rate.csv", index=False)
    for breakdown in breakdowns:
        df = pd.concat(data[breakdown])

        # sort by date
        df = df.sort_values(by=["date"])
        df.to_csv(f"{args.input_dir}/measure_{breakdown}_rate.csv", index=False)
  
   

if __name__ == "__main__":
    main()