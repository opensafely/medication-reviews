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

def checkColumnDict(dic, key):
    if key in dic.keys():
        return dic[key]
    else:
        return key

med_review_type=["allmedrv", "allmedrv12m"]

med_review_dict={
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
    df = pd.read_csv(OUTPUT_DIR / f"correctedagegroupsmeasures/{med_review}_population_rate_agesexstandardgrouped_corrected_standardised.csv", parse_dates=["date"])
    df['percentrate']=df['UK Standard population rate per 100,000']/1000
    print(df)

    plot_measures(df, filename=f"{med_review}_population_rate_standardised", title="", column_to_plot='percentrate', y_label=f"Percentage of people who received a {med_review_dict[med_review]} ", outputfilepath="figures-standardised") #Plot

    for breakdownby in breakdowns:
        df = pd.read_csv(OUTPUT_DIR / f"correctedagegroupsmeasures/{med_review}_{breakdownby}_rate_agesexstandardgrouped_corrected_standardised.csv", parse_dates=["date"])
        df['percentrate']=df['UK Standard population rate per 100,000']/1000
        breakdownbycol=checkColumnDict(columnlookupdict, breakdownby)
        df[breakdownbycol] = df[breakdownbycol].fillna('missing')
        if (breakdownby == "care_home_type"): 
            df=binary_care_home_status(df, numerator_col, 'percentrate')
            convert_binary(df, 'care_home_type', 'Record of positive care home status', 'No record of positive care home status')
#       if (breakdownby == "care_home_type"): 
#           df=binary_care_home_status(df, numerator_col, 'population',valuecolname="UK Standard population rate per 100,000")
#           convert_binary(df, 'care_home_type', 'Record of positive care home status', 'No record of positive care home status')
        if (breakdownby == "learning_disability"):
            convert_binary(df, 'learning_disability', 'Record of learning disability', 'No record of learning disability')
        if (breakdownby == "nhome"):
            convert_binary(df, 'nhome', 'Record of individual living at a nursing home', 'No record of individual living at a nursing home')
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
        plot_measures(df, filename=f"{med_review}_{breakdownby}_rate_standardised", title="", column_to_plot="percentrate", y_label=f"Percentage of people who received a {med_review_dict[med_review]}", category=breakdownbycol, outputfilepath="figures-standardised")