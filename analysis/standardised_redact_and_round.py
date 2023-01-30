import pandas as pd
from redaction_utils import *
from pathlib import Path
from utilities import *

if not (OUTPUT_DIR / "redacted/standardised").exists():
    Path.mkdir(OUTPUT_DIR / "redacted/standardised")

breakdowns=[
"age_band",
"sex",
"imdQ5",
"region",
"ethnicity",
"nhome",
"learning_disability",
"care_home_type",
"addictive_meds",
"dmards",
"highrisk_meds",
"teratogenic_meds"
]

med_review_type=["smr", "smr12m", "mr", "mr12m", "allmedrv", "allmedrv12m"]

#Redact measures files - Redact counts <=7 then round counts to nearest 5
for med_review in med_review_type:
    if (med_review=="allmedrv"):
        numerator_col="had_anymedrev" # fix as column title doesn't match filename for allmedrv
    elif (med_review=="allmedrv12m"):
        numerator_col="had_anymedrev12m" # fix as column title doesn't match filename for allmedrv
    else:
        numerator_col=f'had_{med_review}'
    df = pd.read_csv(OUTPUT_DIR / f"joined/measure_{med_review}_population_rate.csv", parse_dates=["date"])
    if (med_review=="smr" or med_review=="smr12m"):
        df = df.loc[(df['date'] >= '2020-01-01')] #Filter to only include dates inc and after Jan 2020
    df = redact_small_numbers(df, n=7, rounding_base=5, numerator=numerator_col, denominator="population", rate_column="value", date_column="date")  
    df.to_csv(OUTPUT_DIR / f"redacted/redacted_measure_{med_review}_population_rate.csv", index=False,)

    for breakdownby in breakdowns:
        df = pd.read_csv(OUTPUT_DIR / f"joined/measure_{med_review}_{breakdownby}_rate.csv", parse_dates=["date"])
        if (med_review=="smr" or med_review=="smr12m"):
            df = df.loc[(df['date'] >= '2020-01-01')] #Filter to only include dates inc and after Jan 2020
        df = redact_small_numbers(df, n=7, rounding_base=5, numerator=numerator_col, denominator="population", rate_column="value", date_column="date")  
        df.to_csv(OUTPUT_DIR / f"redacted/redacted_measure_{med_review}_{breakdownby}_rate.csv", index=False,)

#Redact total codeuse counts files - Redact counts >0 and <=7 then round counts to nearest 5
codeusefiles=["totalcodeuse", "totalcodeuse_allmedrev"]
for file in codeusefiles:
    df = pd.read_csv(OUTPUT_DIR / f"{file}.csv")
    df = codeuse_redact_small_numbers(df, n=7, rounding_base=5, column="uses")
    df.to_csv(OUTPUT_DIR / f"redacted/standardised/redacted_{file}.csv", index=False,)
