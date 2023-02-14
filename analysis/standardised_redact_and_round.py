import pandas as pd
from redaction_utils import *
from pathlib import Path
from utilities import *

if not (OUTPUT_DIR / "redacted-standardised").exists():
    Path.mkdir(OUTPUT_DIR / "redacted-standardised")

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

med_review_type=["allmedrv", "allmedrv12m", "smr", "smr12m"]

#Redact measures files - Redact counts <=7 then round counts to nearest 5
for med_review in med_review_type:
    if (med_review=="allmedrv"):
        numerator_col="had_anymedrev" # fix as column title doesn't match filename for allmedrv
    elif (med_review=="allmedrv12m"):
        numerator_col="had_anymedrev12m" # fix as column title doesn't match filename for allmedrv
    else:
        numerator_col=f'had_{med_review}'
    df = pd.read_csv(OUTPUT_DIR / f"correctedagegroupsmeasures/{med_review}_population_rate_agesexstandardgrouped_corrected_standardised.csv", parse_dates=["date"])
    df = redact_small_numbers(df, n=7, rounding_base=5, numerator=numerator_col, denominator="population", rate_column="value", date_column="date")  
    df.to_csv(OUTPUT_DIR / f"redacted-standardised/redacted_standardised_measure_{med_review}_population_rate.csv", index=False,)

    for breakdownby in breakdowns:
        df = pd.read_csv(OUTPUT_DIR / f"correctedagegroupsmeasures/{med_review}_{breakdownby}_rate_agesexstandardgrouped_corrected_standardised.csv", parse_dates=["date"])
        df = redact_small_numbers(df, n=7, rounding_base=5, numerator=numerator_col, denominator="population", rate_column="value", date_column="date")  
        df.to_csv(OUTPUT_DIR / f"redacted-standardised/redacted_standardised_measure_{med_review}_{breakdownby}_rate.csv", index=False,)
