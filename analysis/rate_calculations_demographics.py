import numpy as np
import pandas as pd

def load_standard_pop():
    path = "analysis/european_standard_population.csv"
    ## European standardisation data from:
    # from urllib.request import urlopen
    # url = "https://www.opendata.nhs.scot/dataset/4dd86111-7326-48c4-8763-8cc4aa190c3e/resource/edee9731-daf7-4e0d-b525-e4c1469b8f69/download/european_standard_population.csv"
    # with urlopen(url) as f:
    #     pd.read_csv(f).to_csv(path, index=False)
    standard_pop = pd.read_csv(path)
    standard_pop["AgeGroup"] = standard_pop["AgeGroup"].str.replace(" years", "")
    standard_pop = standard_pop.set_index("AgeGroup")["EuropeanStandardPopulation"]
    standard_pop = standard_pop / standard_pop.sum()
    return standard_pop

def calculate_rates(df, numeratorcol, denominatorcol):
    rates = (df[numeratorcol] / df[denominatorcol]) * 100000
    return rates.round()

def get_data(file, numeratorcol, denominatorcol, group_by, demographic_var):
    p = f"output/joined/measure_{file}.csv"
    by_age = pd.read_csv(p, usecols=["date", numeratorcol, denominatorcol] + group_by)
    by_age["date"] = pd.to_datetime(by_age["date"])

    #remove people with "Missing" in demographic vars
    by_age = by_age[by_age[demographic_var] != "Missing"]

    #by_age = by_age.set_index(["date", group_by])
    #totals = by_age.groupby("date").sum()
    #return by_age, totals
    return by_age

def standardise_rates_apply(by_age_row, standard_pop):
    row_age_group = by_age_row['AgeGroup']
    row_sex_group = by_age_row['sex']
    print (row_age_group)
    print (row_sex_group)

    if row_age_group == 'missing' or row_sex_group == 'missing':
        row_standardised_rate = np.nan
        return row_standardised_rate
    else:
        row_standardised_rate = by_age_row['age_rates'] * standard_pop.loc[(standard_pop["age_stand"]==row_age_group) & (standard_pop["sex"]==row_sex_group), "uk_pop"]
        return row_standardised_rate


def redact_small_numbers(df, numeratorcol, denominatorcol):
    mask_n = df[numeratorcol].isin([1, 2, 3, 4, 5])
    mask_d = df[denominatorcol].isin([1, 2, 3, 4, 5])
    mask = mask_n | mask_d
    df.loc[mask, :] = np.nan
    return df


def make_table(standard_pop, file, numeratorcol, denominatorcol, group_by, demographic_var, redact=True):
    by_age = get_data(file, numeratorcol, denominatorcol, group_by, demographic_var)
    by_age['age_rates'] = calculate_rates(by_age, numeratorcol, denominatorcol)
    by_age["European Standard population rate per 100,000"] = by_age.apply(
        standardise_rates_apply, standard_pop=standard_pop, axis=1)
    by_age.drop(['age_rates'], axis=1, inplace=True)
    standardised_totals = by_age.groupby(
        ["date", demographic_var]).sum().reset_index()
    if redact:
        standardised_totals = redact_small_numbers(standardised_totals, numeratorcol, denominatorcol)
    return standardised_totals

def checkColumnDict(dic, key):
    if key in dic.keys():
        return dic[key]
    else:
        return key       

def main():
    breakdowns=[
    #"age_band",
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

    for breakdownby in breakdowns:
        file=f"allmedrv_{breakdownby}_rate_agestandardgrouped"
        breakdownbycol=checkColumnDict(columnlookupdict, breakdownby)
        numeratorcol="had_anymedrev"
        denominatorcol="population"
        group_by=["AgeGroup", breakdownbycol]
        standard_pop=load_standard_pop()

        df = make_table(standard_pop, file, numeratorcol, denominatorcol, group_by, demographic_var = breakdownbycol)
        df.to_csv(f"output/joined/{file}_table.csv")

        file=f"allmedrv12m_{breakdownby}_rate_agestandardgrouped"
        breakdownbycol=checkColumnDict(columnlookupdict, breakdownby)
        numeratorcol="had_anymedrev12m"
        denominatorcol="population"
        group_by=["AgeGroup", breakdownbycol]
        standard_pop=load_standard_pop()

        df = make_table(standard_pop, file, numeratorcol, denominatorcol, group_by, demographic_var = breakdownbycol)
        df.to_csv(f"output/joined/{file}_table.csv")

main()