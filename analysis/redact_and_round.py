import pandas as pd
from redaction_utils import *
from pathlib import Path
from utilities import *

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

#Redact measures files - Redact counts <=7 then round counts to nearest 5
for med_review in med_review_type:
    df = pd.read_csv(OUTPUT_DIR / f"joined/measure_{med_review}_population_rate.csv", parse_dates=["date"])
    if (med_review=="smr"):
        df = df.loc[(df['date'] >= '2020-01-01')] #Filter to only include dates inc and after Jan 2020
    
    df = redact_small_numbers(df, n=7, rounding_base=5, numerator=f'had_{med_review}', denominator="population", rate_column="value", date_column="date")  
   
    df.to_csv(OUTPUT_DIR / f"redacted/redacted_measure_{med_review}_population_rate.csv", index=False,)
    for breakdownby in breakdowns:
        df = pd.read_csv(OUTPUT_DIR / f"joined/measure_{med_review}_{breakdownby}_rate.csv", parse_dates=["date"])
        if (med_review=="smr"):
            df = df.loc[(df['date'] >= '2020-01-01')] #Filter to only include dates inc and after Jan 2020
        
        df = redact_small_numbers(df, n=7, rounding_base=5, numerator=f'had_{med_review}', denominator="population", rate_column="value", date_column="date")  
   
 
        df.to_csv(OUTPUT_DIR / f"redacted/redacted_measure_{med_review}_{breakdownby}_rate.csv", index=False,)


#Redact total codeuse counts files - Redact counts >0 and <=7 then round counts to nearest 5
codeusefiles=["totalcodeuse", "totalcodeuse_allmedrev"]
for file in codeusefiles:
    df = pd.read_csv(OUTPUT_DIR / f"{file}.csv")
    df = codeuse_redact_small_numbers(df, n=7, rounding_base=5, column="uses")
    df.to_csv(OUTPUT_DIR / f"redacted/redacted_{file}.csv", index=False,)
