import pandas as pd
from utilities import *

if not (OUTPUT_DIR / "figures").exists():
    Path.mkdir(OUTPUT_DIR / "figures")

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
        print("Present, ", end =" ")
        return dic[key]
    else:
        return key

med_review_type=["smr", "smr12m", "mr", "mr12m", "allmedrv", "allmedrv12m"]

med_review_dict={
    "smr" : "structured medication review",
    "mr" : "medication review",
    "allmedrv": "medication review",
    "smr12m" : "structured medication review in preceding 12 months",
    "mr12m" : "medication review  in preceding 12 months",
    "allmedrv12m": "medication review in preceding 12 months",
}

for med_review in med_review_type:
    if (med_review=="allmedrv"):
        numerator_col="had_anymedrev" # fix as column title doesn't match filename for allmedrv
    elif (med_review=="allmedrv12m"):
        numerator_col="had_anymedrev12m" # fix as column title doesn't match filename for allmedrv
    else:
        numerator_col=f'had_{med_review}'
    df = pd.read_csv(OUTPUT_DIR / f"redacted/redacted_measure_{med_review}_population_rate.csv", parse_dates=["date"])
    calculate_rate(df, numerator_col, 'population', rate_per=1000, round_rate=False) #Add column for rate per 1000 patients
    plot_measures(df, filename=f"{med_review}_population_rate_perthousand", title="", column_to_plot="rate", y_label=f"People who received a {med_review_dict[med_review]} per 1000 registered patients") #Plot

    calculate_rate(df, numerator_col, 'population', rate_per=100, round_rate=False) #Add column for %
    plot_measures(df, filename=f"{med_review}_population_rate_percentage", title="", column_to_plot="rate", y_label="Percentage") #Plot

    for breakdownby in breakdowns:
        df = pd.read_csv(OUTPUT_DIR / f"redacted/redacted_measure_{med_review}_{breakdownby}_rate.csv", parse_dates=["date"])
        breakdownbycol=checkColumnDict(columnlookupdict, breakdownby)
        df[breakdownbycol] = df[breakdownbycol].fillna('missing')
        if (breakdownby == "care_home_type"): 
            df=binary_care_home_status(df, numerator_col, 'population')
            convert_binary(df, 'care_home_type', 'Record of positive care home status', 'No record of positive care home status')
        if (breakdownby == "learning_disability"):
            convert_binary(df, 'learning_disability', 'Record of learning disability', 'No record of learning disability')
        if (breakdownby == "nhome"):
            convert_binary(df, 'nhome', 'Record of individual living at a nursing home', 'No record of individual living at a nursing home')
        if (breakdownby == "addictivemeds_last12m"):
            convert_binary(df, 'addictivemeds_last12m', 'addictive meds yes', 'addictive meds no')
        if (breakdownby == "sex"):
            df = relabel_sex(df)
        #Add column for rate per 1000 patients
        calculate_rate(df, numerator_col, 'population', rate_per=1000, round_rate=False)
        plot_measures(df, filename=f"{med_review}_{breakdownby}_rate_perthousand", title="", column_to_plot="rate", y_label=f"People who received a {med_review_dict[med_review]} per 1000 registered patients", category=breakdownbycol)

        calculate_rate(df, numerator_col, 'population', rate_per=100, round_rate=False)
        plot_measures(df, filename=f"{med_review}_{breakdownby}_rate_percentage", title="", column_to_plot="rate", y_label=f"Percentage of people who received a {med_review_dict[med_review]}", category=breakdownbycol)


    #Plot deciles chart
    df = pd.read_csv(OUTPUT_DIR / f"joined/deciles_table_{med_review}_practice_rate.csv", parse_dates=["date"])
    df['rateperthousand']=df['value']*1000
    plot_measures(df, filename=f"deciles_chart_{med_review}_practice_rate_perthousand", title="", column_to_plot="rateperthousand", y_label=f"People who received a {med_review_dict[med_review]} per 1000 registered patients", category="percentile", deciles=True)

    df['percentage']=df['value']*100
    plot_measures(df, filename=f"deciles_chart_{med_review}_practice_rate_percentage", title="", column_to_plot="percentage", y_label=f"Percentage of people who received a {med_review_dict[med_review]}", category="percentile", deciles=True)
