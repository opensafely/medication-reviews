# load each input file and count the number of unique patients and number of events
from pathlib import Path
from report_utils import match_input_files, get_date_input_file, save_to_json
import pandas as pd
import argparse
import numpy as np

def round_to_nearest_100(x):
    return int(round(x, -2))

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, required=True)
    parser.add_argument('--output_dir', type=str, required=True)
    return parser.parse_args()

def get_unique_patients(df):
    return df.loc[:,"patient_id"].unique()

def get_number_of_events(df):
    return df.loc[:,"event_measure"].sum()

def get_number_practices(df):
    return df.loc[:,"practice"].unique()

def main():
    args = parse_args()

    patients = []
    practices = []
    events = {}
    
    for file in Path(args.input_dir).iterdir():
        if match_input_files(file.name):
            date = get_date_input_file(file.name)
            df = pd.read_csv(file)
            df["date"] = date
            num_events = get_number_of_events(df)
            events[date] = num_events
            unique_patients = get_unique_patients(df)
            patients.extend(unique_patients)
            unique_practices = get_number_practices(df)
            practices.extend(unique_practices)

    total_events = round_to_nearest_100(sum(events.values()))
    total_patients = round_to_nearest_100(len(np.unique(patients)))
    total_practices = round_to_nearest_100(len(np.unique(practices)))
    events_in_latest_period = round_to_nearest_100(events[max(events.keys())])

    save_to_json({"total_events": total_events, "total_patients": total_patients, "events_in_latest_period": events_in_latest_period, "total_practices": total_practices}, f"{args.output_dir}/event_counts.json")

if __name__ == "__main__":
    main()
