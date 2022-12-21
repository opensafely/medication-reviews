import pandas as pd
from pathlib import Path
#from utilities import *

#if not (OUTPUT_DIR / "correctedagegroupsmeasures").exists():
    #Path.mkdir(OUTPUT_DIR / "correctedagegroupsmeasures")

BASE_DIR = Path(__file__).parents[1]
OUTPUT_DIR = BASE_DIR / "output"
ANALYSIS_DIR = BASE_DIR / "analysis"
CODELIST_DIR = BASE_DIR / "codelists"

#Open files


#Update age standardised group


#Update age plot group

#Save as CSV

def regroupAgeGroup(df, demographic, numerator_column):


def main():
    breakdowns=[
        "population",
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
    columnlookupdict_medrevtype={
        "allmedrv": "had_anymedrev",
        "allmedrv12m": "had_anymedrev12m"
    }
    med_review_type=["allmedrv", "allmedrv12m"]

    for med_review in med_review_type:
        for breakdownby in breakdowns:
            filename=f"measure_{med_review}_{breakdownby}_rate_agesexstandardgrouped.csv"
            breakdownbycol=columnlookupdict.get(breakdownby, breakdownby)
            numerator_column=columnlookupdict_medrevtype.get(med_review, med_review)
            df = pd.read_csv(OUTPUT_DIR / f"joined/{filename}", parse_dates=["date"])
            regroupAgeGroup(df, breakdownbycol, numerator_column)
            print (df.head(20))

main()