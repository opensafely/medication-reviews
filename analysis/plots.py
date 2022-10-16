import pandas as pd
from utilities import *
from redaction_utils import *

if not (OUTPUT_DIR / "figures").exists():
    Path.mkdir(OUTPUT_DIR / "figures")

if not (OUTPUT_DIR / "redacted").exists():
    Path.mkdir(OUTPUT_DIR / "redacted")

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

#Redact counts <=7 then round counts to nearest 5
for med_review in med_review_type:
    df = pd.read_csv(OUTPUT_DIR / f"joined/measure_{med_review}_population_rate.csv", parse_dates=["date"])
    df[f'had_{med_review}'] = drop_and_round(df[f'had_{med_review}'], base=5, threshold=7)
    df['population'] = drop_and_round(df['population'], base=5, threshold=7)
    df.to_csv(OUTPUT_DIR / f"redacted/redacted_measure_{med_review}_population_rate.csv", index=False,)
    for breakdownby in breakdowns:
        df = pd.read_csv(OUTPUT_DIR / f"joined/measure_{med_review}_{breakdownby}_rate.csv", parse_dates=["date"])
        df[f'had_{med_review}'] = drop_and_round(df[f'had_{med_review}'], base=5, threshold=7)
        df['population'] = drop_and_round(df['population'], base=5, threshold=7)
        df.to_csv(OUTPUT_DIR / f"redacted/redacted_measure_{med_review}_population_rate.csv", index=False,)

for med_review in med_review_type:
    df = pd.read_csv(OUTPUT_DIR / f"joined/measure_{med_review}_population_rate.csv", parse_dates=["date"])
    #Add column for rate per 1000 patients
    calculate_rate(df, f'had_{med_review}', 'population', rate_per=1000, round_rate=False)
    #Plot
    plot_measures(df, filename=f"{med_review}_population_rate", title="", column_to_plot="rate", y_label="Rate per 1000")
    for breakdownby in breakdowns:
        df = pd.read_csv(OUTPUT_DIR / f"joined/measure_{med_review}_{breakdownby}_rate.csv", parse_dates=["date"])
        df[breakdownby] = df[breakdownby].fillna('missing')
        if (breakdownby == "care_home_type"): 
            df=binary_care_home_status(df, f'had_{med_review}', 'population')
            convert_binary(df, 'care_home_type', 'Record of positive care home status', 'No record of positive care home status')
        if (breakdownby == "learning_disability"):
            convert_binary(df, 'learning_disability', 'Record of learning disability', 'No record of learning disability')
        if (breakdownby == "nhome"):
            convert_binary(df, 'nhome', 'Record of individual living at a nursing home', 'No record of individual living at a nursing home')
        #Add column for rate per 1000 patients
        calculate_rate(df, f'had_{med_review}', 'population', rate_per=1000, round_rate=False)
        plot_measures(df, filename=f"{med_review}_{breakdownby}_rate", title="", column_to_plot="rate", y_label="Rate per 1000", category=breakdownby)
