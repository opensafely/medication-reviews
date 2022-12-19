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

def get_data(file, numeratorcol, denominatorcol, group_by):
    p = f"output/joined/measure_{file}.csv"
    by_age = pd.read_csv(p, usecols=["date", numeratorcol, denominatorcol, group_by])
    by_age["date"] = pd.to_datetime(by_age["date"])
    by_age = by_age.set_index(["date", group_by])
    totals = by_age.groupby("date").sum()
    return by_age, totals


def calculate_rates(df, numeratorcol, denominatorcol):
    rates = (df[numeratorcol] / df[denominatorcol]) * 100000
    return rates.round()


def standardise_rates(standard_pop, by_age, numeratorcol, denominatorcol):
    rates = calculate_rates(by_age, numeratorcol, denominatorcol)
    standardised_rates = rates * standard_pop
    standardised_totals = standardised_rates.groupby("date").sum()
    return standardised_totals


def redact_small_numbers(df, numeratorcol, denominatorcol):
    mask_n = df[numeratorcol].isin([1, 2, 3, 4, 5])
    mask_d = df[denominatorcol].isin([1, 2, 3, 4, 5])
    mask = mask_n | mask_d
    df.loc[mask, :] = np.nan
    return df


def make_table(standard_pop, file, numeratorcol, denominatorcol, group_by):
    by_age, totals = get_data(file, numeratorcol, denominatorcol, group_by)
    rates = calculate_rates(totals, numeratorcol, denominatorcol)
    rates.name = "Crude rate per 100,000 population"
    standardised_rates = standardise_rates(standard_pop, by_age, numeratorcol, denominatorcol)
    standardised_rates.name = "European Standard population rate per 100,000"
    df = pd.concat([totals, rates, standardised_rates], axis=1)
    df = redact_small_numbers(df, numeratorcol, denominatorcol)
    return df

def main():
    file="allmedrv_population_rate_agestandardgrouped"
    numeratorcol="had_anymedrev"
    denominatorcol="population"
    group_by="AgeGroup"
    standard_pop=load_standard_pop()
    df = make_table(standard_pop, file, numeratorcol, denominatorcol, group_by)
    df.to_csv(f"output/{file}_table.csv")

main()
