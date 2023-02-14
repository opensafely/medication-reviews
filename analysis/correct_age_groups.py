import pandas as pd
from pathlib import Path

def regroupAgeGroup(df, demographic, numerator_column):
    df[demographic]=df[demographic].fillna('Missing')
    df["AgeGroup"] = df["AgeGroup"].replace({'15-19': '18-24', '20-24': '18-24'})
    if (demographic!="sex" and demographic!="population"):
        df = df.groupby(["AgeGroup", "sex", demographic, "date"], as_index=False)[[numerator_column, 'population']].sum()
    else:
        df = df.groupby(["AgeGroup", "sex", "date"], as_index=False)[[numerator_column, 'population']].sum()
    df = df.sort_values(by=['date', 'AgeGroup', 'sex', demographic])
    df["value"]=df[numerator_column]/df["population"]
    return df

def regroupage_band(df, numerator_column):
    df["age_band"] = df["age_band"].replace({'0-19': '18-29', '20-29': '18-29'})
    df = df.groupby(["sex", "age_band", "date"], as_index=False)[[numerator_column, 'population']].sum()
    df = df.sort_values(by=['date', 'age_band', 'sex'])
    df["value"]=df[numerator_column]/df["population"]
    return df

def main():
    BASE_DIR = Path(__file__).parents[1]
    OUTPUT_DIR = BASE_DIR / "output"
    ANALYSIS_DIR = BASE_DIR / "analysis"
    CODELIST_DIR = BASE_DIR / "codelists"

    if not (OUTPUT_DIR / "correctedagegroupsmeasures").exists():
        Path.mkdir(OUTPUT_DIR / "correctedagegroupsmeasures")
    breakdowns=[
        "population",
        "age_band",
        "sex",
        "imdQ5",
        "region",
        "ethnicity",
        "ethnicity16",
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
        "allmedrv12m": "had_anymedrev12m",
        "smr": "had_smr",
        "smr12m": "had_smr12m"
    }
    med_review_type=["allmedrv", "allmedrv12m", "smr", "smr12m"]

    for med_review in med_review_type:
        for breakdownby in breakdowns:
            filename=f"measure_{med_review}_{breakdownby}_rate_agesexstandardgrouped.csv"
            breakdownbycol=columnlookupdict.get(breakdownby, breakdownby)
            numerator_column=columnlookupdict_medrevtype.get(med_review, med_review)
            if (breakdownby=='age_band'):
                df = pd.read_csv(OUTPUT_DIR / f"joined/{filename}", parse_dates=["date"], usecols=["sex", breakdownbycol, numerator_column, "population", "date"])
                df = regroupage_band(df, numerator_column)
            else:
                df = pd.read_csv(OUTPUT_DIR / f"joined/{filename}", parse_dates=["date"], usecols=["AgeGroup", "sex", breakdownbycol, numerator_column, "population", "date"])
                df = regroupAgeGroup(df, breakdownbycol, numerator_column)
            df.to_csv(OUTPUT_DIR / f"correctedagegroupsmeasures/measure_{med_review}_{breakdownby}_rate_agesexstandardgrouped_corrected.csv", index=False,)

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   main()