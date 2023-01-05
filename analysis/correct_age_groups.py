import pandas as pd
from pathlib import Path
#from utilities import *

from pathlib import Path

BASE_DIR = Path(__file__).parents[1]
OUTPUT_DIR = BASE_DIR / "output"
ANALYSIS_DIR = BASE_DIR / "analysis"
CODELIST_DIR = BASE_DIR / "codelists"

if not (OUTPUT_DIR / "correctedagegroupsmeasures").exists():
    Path.mkdir(OUTPUT_DIR / "correctedagegroupsmeasures")



#Open files


#Update age standardised group


#Update age plot group

#Save as CSV

def regroupAgeGroup(df, demographic, numerator_column):
    df["AgeGroup"] = df["AgeGroup"].replace({'15-19': '18-24', '20-24': '18-24'})
    df = df.groupby(["AgeGroup", "sex", demographic, "date"], as_index=False)[[numerator_column, 'population']].sum()
    df = df.sort_values(by=['date', 'AgeGroup', 'sex', demographic])
    #RECALCULATE RATE
    df["value"]=df[numerator_column]/df["population"]
    return df

def regroupage_band(df, demographic, numerator_column):
    df["age_band"] = df["age_band"].replace({'0-19': '18-29', '20-29': '18-29'})
    df = df.groupby(["AgeGroup", "sex", "age_band", "date"], as_index=False)[[numerator_column, 'population']].sum()
    #df = df.sort_values(by=['date', 'AgeGroup', 'sex', demographic])
    return df

def main():
    breakdowns=[
        "population",
        "age_band",
        #"sex",
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
            df = pd.read_csv(OUTPUT_DIR / f"joined/{filename}", parse_dates=["date"], usecols=["AgeGroup", "sex", breakdownbycol, numerator_column, "population", "date"])
            df = regroupAgeGroup(df, breakdownbycol, numerator_column)
            if (breakdownby=='age_band'):
                df = regroupage_band(df, breakdownbycol, numerator_column)
            if (breakdownby=='sex'):
                print('here')
            df.to_csv(OUTPUT_DIR / f"correctedagegroupsmeasures/measure_{med_review}_{breakdownby}_rate_agesexstandardgrouped_corrected.csv", index=False,)
main()