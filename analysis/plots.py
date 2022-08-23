import pandas as pd
from utilities import *

if not (OUTPUT_DIR / "figures").exists():
    Path.mkdir(OUTPUT_DIR / "figures")


breakdowns=[
"age_band",
"sex",
"imdQ5",
"region",
"ethnicity",
"nhome",
"learning_disability",
"care_home_type"
]

med_review_type=["smr", "mr"]
for med_review in med_review_type:
    df = pd.read_csv(OUTPUT_DIR / f"joined/measure_{med_review}_population_rate.csv", parse_dates=["date"])
    plot_measures(df, filename=f"{med_review}_population_rate", title="", column_to_plot="value", y_label="Rate")
    for breakdownby in breakdowns:
        df = pd.read_csv(OUTPUT_DIR / f"joined/measure_{med_review}_{breakdownby}_rate.csv", parse_dates=["date"])
        df[breakdownby] = df[breakdownby].fillna('missing')
        if (breakdownby == "care_home_type"): 
            binary_care_home_status(df)
        plot_measures(df, filename=f"{med_review}_{breakdownby}_rate", title="", column_to_plot="value", y_label="Rate", category=breakdownby)
