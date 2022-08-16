import pandas as pd
from utilities import *

if not (OUTPUT_DIR / "figures").exists():
    Path.mkdir(OUTPUT_DIR / "figures")

df = pd.read_csv(OUTPUT_DIR / f"joined/measure_smr_population_rate.csv", parse_dates=["date"])
plot_measures(df, filename="smr_population_rate", title="", column_to_plot="value", y_label="Rate")

breakdowns=[
"age_band",
"sex",
"imdQ5",
"region",
"ethnicity",
"learning_disability"
]

for breakdownby in breakdowns:
    df = pd.read_csv(OUTPUT_DIR / f"joined/measure_smr_{breakdownby}_rate.csv", parse_dates=["date"])

    if (breakdownby=="ethnicity"):
        # Dummy data cannot match ethnicity as samples aren't linked - replace blank values with string "missing" 
        df['ethnicity'] = df['ethnicity'].fillna('missing')   

    plot_measures(df, filename=f"smr_{breakdownby}_rate", title="", column_to_plot="value", y_label="Rate", category=breakdownby)
