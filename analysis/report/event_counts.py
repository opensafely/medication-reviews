# load each input file and count the number of unique patients and number of events
from pathlib import Path
from report_utils import match_input_files, get_date_input_file, save_to_json
import pandas as pd
import argparse
import numpy as np

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_dir', type=str, required=True)
    parser.add_argument('--output_dir', type=str, required=True)
    return parser.parse_args()

def get_unique_patients(df):
    return df.loc[:,"patient_id"].unique()

def get_number_of_events(df):
    return df.loc[:,"event_measure"].sum()


def main():
    args = parse_args()

    patients = []
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

    total_events = sum(events.values())
    total_patients = len(np.unique(patients))
    events_in_latest_period = events[max(events.keys())]

    save_to_json({"total_events": int(total_events), "total_patients": int(total_patients), "events_in_latest_period": int(events_in_latest_period)}, f"{args.output_dir}/event_counts.json")

if __name__ == "__main__":
    main()
