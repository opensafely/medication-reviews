import pandas as pd
import argparse
from report_utils import plot_measures, plot_measures_interactive

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--breakdowns", help="codelist to use")
    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    if args.breakdowns != "":

        breakdowns = args.breakdowns.split(",")
    else:
        breakdowns = []
    
  
    df = pd.read_csv(f"output/report/joined/measure_total_rate.csv", parse_dates=["date"])
    df = df.loc[df["value"] != "[Redacted]", :]
    

    
    plot_measures(
    df,
        filename=f"report/plot_measures",
        column_to_plot="value",
        y_label="Rate per 1000",
        as_bar=False,
        category=None,
    )

    plot_measures_interactive(df, filename=f"report/plot_measures", column_to_plot="value", category=None, y_label="Rate per 1000")
  
    for breakdown in breakdowns:
        df = pd.read_csv(
            f"output/report/joined/measure_{breakdown}_rate.csv", parse_dates=["date"]
        )
        df = df.loc[df["value"] != "[Redacted]", :]
        df = df.sort_values(by=["date"])
        

    
        plot_measures(
            df,
            filename=f"report/plot_measures_{breakdown}",
            column_to_plot="value",
            y_label="Rate per 1000",
            as_bar=False,
            category=breakdown,
        )
        plot_measures_interactive(df, filename=f"report/plot_measures_{breakdown}", column_to_plot="value", category=breakdown, y_label="Rate per 1000")
  
    
if __name__ == "__main__":
    main()