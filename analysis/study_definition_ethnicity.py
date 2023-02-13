from cohortextractor import StudyDefinition, patients

from codelists import *

start_date = "2019-04-01"
end_date = "2022-03-01"

study = StudyDefinition(
    index_date=end_date,
    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
        "rate": "uniform",
        "incidence": 0.5,
    },
    population=patients.all(),
    ethnicity=patients.categorised_as(
        {
            "Missing": "DEFAULT",
            "White": "eth='1' OR (NOT eth AND ethnicity_sus='1')",
            "Mixed": "eth='2' OR (NOT eth AND ethnicity_sus='2')",
            "South Asian": "eth='3' OR (NOT eth AND ethnicity_sus='3')",
            "Black": "eth='4' OR (NOT eth AND ethnicity_sus='4')",
            "Other": "eth='5' OR (NOT eth AND ethnicity_sus='5')",
        },
        return_expectations={
            "category": {
                "ratios":
                    {
                        "White": 0.2,
                        "Mixed": 0.2,
                        "South Asian": 0.2,
                        "Black": 0.2,
                        "Other": 0.2
                    }
                },
            "incidence": 0.4,
        },
        ethnicity_sus=patients.with_ethnicity_from_sus(
            returning="group_6",
            use_most_frequent_code=True,
            return_expectations={
                "category": {
                    "ratios": {
                        "1": 0.2,
                        "2": 0.2,
                        "3": 0.2,
                        "4": 0.2,
                        "5": 0.2
                    }
                },
                "incidence": 0.4,
            },
        ),
        eth=patients.with_these_clinical_events(
            ethnicity_codes,
            returning="category",
            find_last_match_in_period=True,
            on_or_before="index_date",
            return_expectations={
                "category": {
                    "ratios": {
                        "1": 0.4,
                        "2": 0.4,
                        "3": 0.2,
                        "4": 0.2,
                        "5": 0.2
                    }
                },
                "incidence": 0.75,
            },
        ),
    ),
    ethnicity16=patients.categorised_as(
        {
            "Missing": "DEFAULT",
            "White - British": "eth16='1' OR (NOT eth16 AND ethnicity_sus16='1')",
            "White - Irish": "eth16='2' OR (NOT eth16 AND ethnicity_sus16='2')",
            "White - Any other White background": "eth16='3' OR (NOT eth16 AND ethnicity_sus16='3')",
            "Mixed - White and Black Caribbean": "eth16='4' OR (NOT eth16 AND ethnicity_sus16='4')",
            "Mixed - White and Black African": "eth16='5' OR (NOT eth16 AND ethnicity_sus16='5')",
            "Mixed - White and Asian": "eth16='6' OR (NOT eth16 AND ethnicity_sus16='6')",
            "Mixed - Any other mixed background": "eth16='7' OR (NOT eth16 AND ethnicity_sus16='7')",
            "Asian or Asian British - Indian": "eth16='8' OR (NOT eth16 AND ethnicity_sus16='8')",
            "Asian or Asian British - Pakistani": "eth16='9' OR (NOT eth16 AND ethnicity_sus16='9')",
            "Asian or Asian British - Bangladeshi": "eth16='10' OR (NOT eth16 AND ethnicity_sus16='10')",
            "Asian or Asian British - Any other Asian background": "eth16='11' OR (NOT eth16 AND ethnicity_sus16='11')",
            "Black or Black British - Caribbean": "eth16='12' OR (NOT eth16 AND ethnicity_sus16='12')",
            "Black or Black British - African": "eth16='13' OR (NOT eth16 AND ethnicity_sus16='13')",
            "Black or Black British - Any other Black background": "eth16='14' OR (NOT eth16 AND ethnicity_sus16='14')",
            "Other Ethnic Groups - Chinese": "eth16='15' OR (NOT eth16 AND ethnicity_sus16='15')",
            "Other Ethnic Groups - Any other ethnic group": "eth16='16' OR (NOT eth16 AND ethnicity_sus16='16')",
        },
        return_expectations={
            "category": {
                "ratios":
                    {
                        "White - British": 0.2,
                        "White - Irish": 0.1,
                        "White - Any other White background": 0.1,
                        "Mixed - White and Black Caribbean": 0.1,
                        "Mixed - White and Black African": 0.1,
                        "Mixed - White and Asian": 0.1,
                        "Mixed - Any other mixed background": 0.03,
                        "Asian or Asian British - Indian": 0.03,
                        "Asian or Asian British - Pakistani": 0.03,
                        "Asian or Asian British - Bangladeshi": 0.03,
                        "Asian or Asian British - Any other Asian background": 0.03,
                        "Black or Black British - Caribbean": 0.03,
                        "Black or Black British - African": 0.03,
                        "Black or Black British - Any other Black background": 0.03,
                        "Other Ethnic Groups - Chinese": 0.03,
                        "Other Ethnic Groups - Any other ethnic group": 0.03
                    }
                },
            "incidence": 0.4,
        },
        ethnicity_sus16=patients.with_ethnicity_from_sus(
            returning="group_16",
            use_most_frequent_code=True,
            return_expectations={
                "category": {
                    "ratios": {
                        "1": 0.2,
                        "2": 0.1,
                        "3": 0.1,
                        "4": 0.1,
                        "5": 0.1,
                        "6": 0.1,
                        "7": 0.03,
                        "8": 0.03,
                        "9": 0.03,
                        "10": 0.03,
                        "11": 0.03,
                        "12": 0.03,
                        "13": 0.03,
                        "14": 0.03,
                        "15": 0.03,
                        "16": 0.03
                    }
                },
                "incidence": 0.4,
            },
        ),
        eth16=patients.with_these_clinical_events(
            ethnicity_codes_16,
            returning="category",
            find_last_match_in_period=True,
            on_or_before="index_date",
            return_expectations={
                "category": {
                    "ratios": {
                        "1": 0.2,
                        "2": 0.1,
                        "3": 0.1,
                        "4": 0.1,
                        "5": 0.1,
                        "6": 0.1,
                        "7": 0.03,
                        "8": 0.03,
                        "9": 0.03,
                        "10": 0.03,
                        "11": 0.03,
                        "12": 0.03,
                        "13": 0.03,
                        "14": 0.03,
                        "15": 0.03,
                        "16": 0.03
                    }
                },
                "incidence": 0.75,
            },
        ),
    ),
)
