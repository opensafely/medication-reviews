import numpy as np
import pandas as pd

def load_standard_pop():
    path = "analysis/ons_pop_stand.csv"
    ## UK standardisation data from ONS
    standard_pop = pd.read_csv(path)
    # Remove trailing text in age column
    standard_pop["age_stand"] = standard_pop["age_stand"].str.replace(" y", "")
    standard_pop["sex"] = standard_pop["sex"].str.replace("Female", "F")
    standard_pop["sex"] = standard_pop["sex"].str.replace("Male", "M")

    # Total population
    total_standardpop = standard_pop
    total_standardpop = total_standardpop.loc[(total_standardpop['sex'] == "Total") & (total_standardpop['age_stand'] == "Total")]
    total_standardpop = total_standardpop.reset_index(drop=True)
    total_standardpop = total_standardpop.loc[0]['uk_pop']

    # Filter out for age sex standardisation
    agesex_standardpop=standard_pop
    agesex_standardpop = agesex_standardpop.loc[(agesex_standardpop['age_stand'] != "Total")]
    agesex_standardpop = agesex_standardpop.loc[(agesex_standardpop['sex'] != "Total")]
    agesex_standardpop['uk_pop_ratio'] = agesex_standardpop['uk_pop']/total_standardpop
    agesex_standardpop = agesex_standardpop.drop(columns=['uk_pop'])

    # Filter out for age standardisation
    age_standardpop=standard_pop
    age_standardpop = age_standardpop.loc[(age_standardpop['sex'] == "Total")]
    age_standardpop = age_standardpop.loc[(age_standardpop['age_stand'] != "Total")]
    age_standardpop['uk_pop_ratio'] = age_standardpop['uk_pop']/total_standardpop
    age_standardpop = age_standardpop.drop(columns=['sex', 'uk_pop'])

    # Filter out for sex standardisation
    sex_standardpop=standard_pop
    sex_standardpop = sex_standardpop.loc[(sex_standardpop['age_stand'] == "Total")]
    sex_standardpop = sex_standardpop.loc[(sex_standardpop['sex'] != "Total")]
    sex_standardpop['uk_pop_ratio'] = sex_standardpop['uk_pop']/total_standardpop
    sex_standardpop = sex_standardpop.drop(columns=['age_stand', 'uk_pop'])

    return agesex_standardpop, sex_standardpop, age_standardpop

def calculate_rates(df, numeratorcol, denominatorcol):
    rates = (df[numeratorcol] / df[denominatorcol]) * 100000
    return rates.round()

def get_data(file, numeratorcol, denominatorcol, group_by, demographic_var):
    p = f"output/correctedagegroupsmeasures/measure_{file}.csv"
    by_age = pd.read_csv(p, usecols=["date", numeratorcol, denominatorcol] + group_by)
    by_age["date"] = pd.to_datetime(by_age["date"])

    #remove people with "Missing" in demographic vars
    #by_age = by_age[by_age[demographic_var] != "Missing"]

    return by_age

def standardise_rates_agesex_apply(by_agesex_row, standard_pop):
    row_age_group = by_agesex_row['AgeGroup']
    row_sex_group = by_agesex_row['sex']
    pop_ratio = standard_pop.loc[(standard_pop["age_stand"]==row_age_group) & (standard_pop["sex"]==row_sex_group), "uk_pop_ratio"]
    if row_age_group == 'missing' or row_sex_group == 'missing':
        row_standardised_rate = np.nan
    else:
        pop_ratio = pop_ratio.values[0]
        row_standardised_rate = by_agesex_row['agesex_rates'] * pop_ratio
    return row_standardised_rate

def standardise_rates_age_apply(by_age_row, standard_pop):
    row_age_group = by_age_row['AgeGroup']
    pop_ratio = standard_pop.loc[(standard_pop["age_stand"]==row_age_group), "uk_pop_ratio"]
    if row_age_group == 'missing':
        row_standardised_rate = np.nan
    else:
        pop_ratio = pop_ratio.values[0]
        row_standardised_rate = by_age_row['agesex_rates'] * pop_ratio
    return row_standardised_rate

def standardise_rates_sex_apply(by_sex_row, standard_pop):
    row_sex_group = by_sex_row['sex']
    pop_ratio = standard_pop.loc[(standard_pop["sex"]==row_sex_group), "uk_pop_ratio"]
    if row_sex_group == 'missing':
        row_standardised_rate = np.nan
    else:
        pop_ratio = pop_ratio.values[0]
        row_standardised_rate = by_sex_row['agesex_rates'] * pop_ratio
    return row_standardised_rate

def redact_small_numbers(df, numeratorcol, denominatorcol):
    mask_n = df[numeratorcol].isin([1, 2, 3, 4, 5])
    mask_d = df[denominatorcol].isin([1, 2, 3, 4, 5])
    mask = mask_n | mask_d
    df.loc[mask, [numeratorcol, denominatorcol, "UK Standard population rate per 100,000"]] = np.nan
    return df


def make_table(standard_pop, file, numeratorcol, denominatorcol, group_by, demographic_var, redact=False, standardisation_type='agesex'):
    by_agesex = get_data(file, numeratorcol, denominatorcol, group_by, demographic_var)
    by_agesex['agesex_rates'] = calculate_rates(by_agesex, numeratorcol, denominatorcol)
    if (standardisation_type=='agesex'):
        by_agesex["UK Standard population rate per 100,000"] = by_agesex.apply(
            standardise_rates_agesex_apply, standard_pop=standard_pop, axis=1)
    elif (standardisation_type=='age'):
        by_agesex["UK Standard population rate per 100,000"] = by_agesex.apply(
            standardise_rates_age_apply, standard_pop=standard_pop, axis=1)
    elif (standardisation_type=='sex'):
        by_agesex["UK Standard population rate per 100,000"] = by_agesex.apply(
            standardise_rates_sex_apply, standard_pop=standard_pop, axis=1)
    by_agesex.drop(['agesex_rates'], axis=1, inplace=True)
    if (demographic_var=="population"):
        standardised_totals = by_agesex.groupby(["date"]).sum().reset_index()
    else:
        standardised_totals = by_agesex.groupby(["date", demographic_var]).sum().reset_index()
    if redact:
        standardised_totals = redact_small_numbers(standardised_totals, numeratorcol, denominatorcol)
    return standardised_totals

def checkColumnDict(dic, key):
    if key in dic.keys():
        return dic[key]
    else:
        return key       

def stand_type(breakdown, agesex_standardpop, sex_standardpop, age_standardpop):
    if (breakdown=='age_band'):
        return 'sex', sex_standardpop, ["sex", breakdown]
    elif (breakdown=='sex'):
        return 'age', age_standardpop, ["AgeGroup", "sex", breakdown]
    else:
        return 'agesex', agesex_standardpop, ["AgeGroup", "sex", breakdown]

def main():
    agesex_standardpop, sex_standardpop, age_standardpop=load_standard_pop()

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

    for breakdownby in breakdowns:
        file=f"allmedrv_{breakdownby}_rate_agesexstandardgrouped_corrected"
        breakdownbycol=checkColumnDict(columnlookupdict, breakdownby)
        numeratorcol="had_anymedrev"
        denominatorcol="population"

        #Type of standardisation
        standardisation_type, standard_pop, group_by=stand_type(breakdownbycol, agesex_standardpop, sex_standardpop, age_standardpop)

        df = make_table(standard_pop, file, numeratorcol, denominatorcol, group_by, demographic_var=breakdownbycol, standardisation_type=standardisation_type)
        df.to_csv(f"output/correctedagegroupsmeasures/{file}_standardised.csv", index=False)

        file=f"allmedrv12m_{breakdownby}_rate_agesexstandardgrouped_corrected"
        numeratorcol="had_anymedrev12m"

        df = make_table(standard_pop, file, numeratorcol, denominatorcol, group_by, demographic_var=breakdownbycol, standardisation_type=standardisation_type)
        df.to_csv(f"output/correctedagegroupsmeasures/{file}_standardised.csv", index=False)

        file=f"smr_{breakdownby}_rate_agesexstandardgrouped_corrected"
        numeratorcol="had_smr"

        df = make_table(standard_pop, file, numeratorcol, denominatorcol, group_by, demographic_var=breakdownbycol, standardisation_type=standardisation_type)
        df.to_csv(f"output/correctedagegroupsmeasures/{file}_standardised.csv", index=False)

        file=f"smr12m_{breakdownby}_rate_agesexstandardgrouped_corrected"
        numeratorcol="had_smr12m"

        df = make_table(standard_pop, file, numeratorcol, denominatorcol, group_by, demographic_var=breakdownbycol, standardisation_type=standardisation_type)
        df.to_csv(f"output/correctedagegroupsmeasures/{file}_standardised.csv", index=False)

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   main()
