import pandas as pd
from utilities import *

if not (OUTPUT_DIR / "figures-standardised").exists():
    Path.mkdir(OUTPUT_DIR / "figures-standardised")

breakdowns=[
"age_band",
"sex",
"imdQ5",
"region",
"ethnicity",
"ethnicity16",
"nhome",
"learning_disability",
"addictive_meds",
"dmards",
"highrisk_meds",
"teratogenic_meds",
"care_home_type"
]

columnlookupdict={
    "addictive_meds": "addictivemeds_last12m",
    "dmards": "dmards_last12m",
    "highrisk_meds": "highriskmeds_last12m",
    "teratogenic_meds": "teratogenicmeds_last12m"
}

med_review_type=["smr", "smr12m", "allmedrv", "allmedrv12m"]

med_review_dict={
    "smr" : "structured medication review",
    "smr12m" : "structured medication review within preceding 12 months",
    "allmedrv": "medication review each month",
    "allmedrv12m": "medication review within preceding 12 months",
}
for med_review in med_review_type:
    if (med_review=="allmedrv"):
        numerator_col="had_anymedrev" # fix as column title doesn't match filename for allmedrv
    elif (med_review=="allmedrv12m"):
        numerator_col="had_anymedrev12m" # fix as column title doesn't match filename for allmedrv
    else:
        numerator_col=f'had_{med_review}'

    if (med_review=="smr" or med_review=="smr12m"):
        smrstartshow=True
    else:
        smrstartshow=False

    df = pd.read_csv(OUTPUT_DIR / f"redacted-standardised/redacted_standardised_measure_{med_review}_population_rate.csv", parse_dates=["date"])
    df['percentrate']=df['UK Standard population rate per 100,000']/1000

    plot_measures(df, filename=f"{med_review}_population_rate_standardised", title="", column_to_plot='percentrate', y_label=f"Percentage of people who received a \n{med_review_dict[med_review]} ", outputfilepath="figures-standardised", smrstart=smrstartshow) #Plot

    for breakdownby in breakdowns:
        df = pd.read_csv(OUTPUT_DIR / f"redacted-standardised/redacted_standardised_measure_{med_review}_{breakdownby}_rate.csv", parse_dates=["date"])
        df['percentrate']=df['UK Standard population rate per 100,000']/1000
        breakdownbycol=columnlookupdict.get(breakdownby, breakdownby)
        df[breakdownbycol] = df[breakdownbycol].fillna('missing')
        if (breakdownby == "care_home_type"): 
            convert_binary(df, 'care_home_type', 'Record of individual living at a care/nursing home', 'No record of individual living at a care/nursing home')
        if (breakdownby == "learning_disability"):
            convert_binary(df, 'learning_disability', 'Record of learning disability', 'No record of learning disability')
        if (breakdownby == "nhome"):
            convert_binary(df, 'nhome', 'Record of individual living at a care/nursing home', 'No record of individual living at a care/nursing home')
        if (breakdownbycol == "addictivemeds_last12m"):
            convert_binary(df, 'addictivemeds_last12m', 'Record of prescription for an addictive medicine', 'No record of prescription for an addictive medicine')
        if (breakdownbycol == "dmards_last12m"):
            convert_binary(df, 'dmards_last12m', 'Record of prescription for a DMARD', 'No record of prescription for a DMARD')
        if (breakdownbycol == "highriskmeds_last12m"):
            convert_binary(df, 'highriskmeds_last12m', 'Record of prescription for a high risk medication', 'No record of prescription for a high risk medication')
        if (breakdownbycol == "teratogenicmeds_last12m"):
            convert_binary(df, 'teratogenicmeds_last12m', 'Record of prescription for a teratogenic medication', 'No record of prescription for a teratogenic medication')
        if (breakdownby == "sex"):
            df = relabel_sex(df)
        #Add column for rate per 1000 patients
        plot_measures(df, filename=f"{med_review}_{breakdownby}_rate_standardised", title="", column_to_plot="percentrate", y_label=f"Percentage of people who received a \n{med_review_dict[med_review]}", category=breakdownbycol, outputfilepath="figures-standardised", smrstart=smrstartshow)
