import pandas as pd
from utilities import *

if not (OUTPUT_DIR / "figures").exists():
    Path.mkdir(OUTPUT_DIR / "figures")

df = pd.read_csv(OUTPUT_DIR / f"joined/measure_smr_population_rate.csv", parse_dates=["date"])
plot_measures(df, filename="smr_population_rate", title="", column_to_plot="value", y_label="Rate")

breakdowns=[
"practice",
"age_band",
"sex",
"imdQ5",
"region",
"ethnicity",
"learning_disability",
"care_home_type"
]

for breakdownby in breakdowns:
    df = pd.read_csv(OUTPUT_DIR / f"joined/measure_smr_{breakdownby}_rate.csv", parse_dates=["date"])

    if (breakdownby=="ethnicity"):
        # Dummy data cannot match ethnicity as none linked samples - 
        df['ethnicity'] = df['ethnicity'].fillna('Missing')
    elif (breakdownby=="care_home_type"):
        df['care_home_type'] = df['care_home_type'].fillna('Missing')   

    plot_measures(df, filename=f"smr_{breakdownby}_rate", title="", column_to_plot="value", y_label="Rate", category=breakdownby)