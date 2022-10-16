import pandas as pd
from redaction_utils import *
from pathlib import Path
from plots import OUTPUT_DIR, breakdowns, med_review_type

if not (OUTPUT_DIR / "redacted").exists():
    Path.mkdir(OUTPUT_DIR / "redacted")

#Redact counts <=7 then round counts to nearest 5
for med_review in med_review_type:
    df = pd.read_csv(OUTPUT_DIR / f"joined/measure_{med_review}_population_rate.csv", parse_dates=["date"])
    df[f'had_{med_review}'] = drop_and_round(df[f'had_{med_review}'], base=5, threshold=7)
    df['population'] = drop_and_round(df['population'], base=5, threshold=7)
    df['value'] = df[f'had_{med_review}']/df['population']
    df.to_csv(OUTPUT_DIR / f"redacted/redacted_measure_{med_review}_population_rate.csv", index=False,)
    for breakdownby in breakdowns:
        df = pd.read_csv(OUTPUT_DIR / f"joined/measure_{med_review}_{breakdownby}_rate.csv", parse_dates=["date"])
        df[f'had_{med_review}'] = drop_and_round(df[f'had_{med_review}'], base=5, threshold=7)
        df['population'] = drop_and_round(df['population'], base=5, threshold=7)
        df['value'] = df[f'had_{med_review}']/df['population']
        df.to_csv(OUTPUT_DIR / f"redacted/redacted_measure_{med_review}_{breakdownby}_rate.csv", index=False,)