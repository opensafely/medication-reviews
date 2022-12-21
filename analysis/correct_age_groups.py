import pandas as pd
from pathlib import Path
#from utilities import *

#if not (OUTPUT_DIR / "correctedagegroupsmeasures").exists():
    #Path.mkdir(OUTPUT_DIR / "correctedagegroupsmeasures")

#Open files


#Load CSV


#Update age standardised group


#Update age plot group

#Save as CSV

def main():
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
    columnlookupdict={
        "addictive_meds": "addictivemeds_last12m",
        "dmards": "dmards_last12m",
        "highrisk_meds": "highriskmeds_last12m",
        "teratogenic_meds": "teratogenicmeds_last12m"
    }
    med_review_type=["smr", "smr12m", "mr", "mr12m", "allmedrv", "allmedrv12m"]

    for med_review in med_review_type:
        df = pd.read_csv(OUTPUT_DIR / f"joined/measure_{med_review}_population_rate.csv", parse_dates=["date"])


    for breakdownby in breakdowns:
        df = pd.read_csv(OUTPUT_DIR / f"redacted/redacted_measure_{med_review}_{breakdownby}_rate.csv", parse_dates=["date"])
        breakdownbycol=checkColumnDict(columnlookupdict, breakdownby)
        df[breakdownbycol] = df[breakdownbycol].fillna('missing')
        if (breakdownby == "care_home_type"): 

main()