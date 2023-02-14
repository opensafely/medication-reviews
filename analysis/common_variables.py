# Sharing common study definition variables
# https://docs.opensafely.org/study-def-tricks/

from cohortextractor import patients, combine_codelists

from codelists import *

combined_addictive_codes = combine_codelists(
    highdoseopioid_codes,
    addictivemeds_codes,
)

common_variables = dict(
    age=patients.age_as_of(
        "last_day_of_month(index_date)",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),
    age_band=patients.categorised_as(
        {
            "missing": "DEFAULT",
            "0-17": """ age >= 0 AND age < 17""",
            "18-29": """ age >=  18 AND age < 30""",
            "30-39": """ age >=  30 AND age < 40""",
            "40-49": """ age >=  40 AND age < 50""",
            "50-59": """ age >=  50 AND age < 60""",
            "60-69": """ age >=  60 AND age < 70""",
            "70-79": """ age >=  70 AND age < 80""",
            "80-89": """ age >=  80 AND age < 90""",
            "90+": """ age >=  90 AND age <= 120""",
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "missing": 0.005,
                    "0-17": 0.035,
                    "18-29": 0.12,
                    "30-39": 0.12,
                    "40-49": 0.12,
                    "50-59": 0.12,
                    "60-69": 0.12,
                    "70-79": 0.12,
                    "80-89": 0.12,
                    "90+": 0.12,
                }
            },
        },
    ),
    AgeGroup=patients.categorised_as(
        {
            "0-17": "age >= 0 AND age < 18",
            "18-24": "age >= 18 AND age < 25",
            "25-29": "age >= 25 AND age < 30",
            "30-34": "age >= 30 AND age < 35",
            "35-39": "age >= 35 AND age < 40",
            "40-44": "age >= 40 AND age < 45",
            "45-49": "age >= 45 AND age < 50",
            "50-54": "age >= 50 AND age < 55",
            "55-59": "age >= 55 AND age < 60",
            "60-64": "age >= 60 AND age < 65",
            "65-69": "age >= 65 AND age < 70",
            "70-74": "age >= 70 AND age < 75",
            "75-79": "age >= 75 AND age < 80",
            "80-84": "age >= 80 AND age < 85",
            "85-89": "age >= 85 AND age < 90",
            "90plus": "age >= 90",
            "missing": "DEFAULT",
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "0-17": 0.06,
                    "18-24": 0.06,
                    "25-29": 0.06,
                    "30-34": 0.06,
                    "35-39": 0.06,
                    "40-44": 0.06,
                    "45-49": 0.06,
                    "50-54": 0.06,
                    "55-59": 0.06,
                    "60-64": 0.06,
                    "65-69": 0.06,
                    "70-74": 0.06,
                    "75-79": 0.06,
                    "80-84": 0.06,
                    "85-89": 0.06,
                    "90plus": 0.06,
                    "missing": 0.04,
                }
            },
        },
    ),
    sex=patients.sex(
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"M": 0.5, "F": 0.5}},
        }
    ),
    imdQ5=patients.categorised_as(
        {
            "Unknown": "DEFAULT",
            "1 (most deprived)": "imd >= 0 AND imd < 32844*1/5",
            "2": "imd >= 32844*1/5 AND imd < 32844*2/5",
            "3": "imd >= 32844*2/5 AND imd < 32844*3/5",
            "4": "imd >= 32844*3/5 AND imd < 32844*4/5",
            "5 (least deprived)": "imd >= 32844*4/5 AND imd <= 32844",
        },
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "Unknown": 0.005,
                    "1 (most deprived)": 0.199,
                    "2": 0.199,
                    "3": 0.199,
                    "4": 0.199,
                    "5 (least deprived)": 0.199,
                }
            },
        },
        imd=patients.address_as_of(
            "last_day_of_month(index_date)",
            returning="index_of_multiple_deprivation",
            round_to_nearest=100,
        )
    ),
    practice=patients.registered_practice_as_of(
        "last_day_of_month(index_date)",
        returning="pseudo_id",
        return_expectations={
            "int": {"distribution": "normal", "mean": 25, "stddev": 5},
            "incidence": 0.5,
        },
    ),
    region=patients.registered_practice_as_of(
        "last_day_of_month(index_date)",
        returning="nuts1_region_name",
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "North East": 0.1,
                    "North West": 0.1,
                    "Yorkshire and The Humber": 0.1,
                    "East Midlands": 0.1,
                    "West Midlands": 0.1,
                    "East": 0.1,
                    "London": 0.1,
                    "South East": 0.1,
                    "South West": 0.1,
                    "missing": 0.1,
                },
            },
        },
    ),
    msoa=patients.address_as_of(
        "last_day_of_month(index_date)",
        returning="msoa",
        return_expectations={
            "rate": "universal",
            "category": {
                "ratios": {
                    "E02000239": 0.3,  #Inland
                    "E02001586": 0.3,  #Inland
                    "E02001263": 0.3,  #Inland
                    "E02004584": 0.05,  #Coastal
                    "E02003979": 0.05,  #Coastal
                },
            },
        },
    ),
    learning_disability=patients.with_these_clinical_events(
        learning_disability_codes,
        on_or_before="last_day_of_month(index_date)",
        returning="binary_flag",
        return_expectations={
            "incidence": 0.01,
        },
    ),
    care_home_type=patients.care_home_status_as_of(
        "last_day_of_month(index_date)",
        categorised_as={
            "CareHome": """
              IsPotentialCareHome
              AND LocationDoesNotRequireNursing='Y'
              AND LocationRequiresNursing='N'
            """,
            "NursingHome": """
              IsPotentialCareHome
              AND LocationDoesNotRequireNursing='N'
              AND LocationRequiresNursing='Y'
            """,
            "CareOrNursingHome": "IsPotentialCareHome",
            "PrivateHome": "NOT IsPotentialCareHome",
            "Default": "DEFAULT",
        },
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"CareHome": 0.30, "NursingHome": 0.10, "CareOrNursingHome": 0.10, "PrivateHome":0.45, "":0.05},},
        },
    ),
    nhome=patients.with_these_clinical_events(
        nhse_care_homes_codes,
        returning="binary_flag",
        on_or_before="last_day_of_month(index_date)",
        return_expectations={"incidence": 0.2},
    ),
    femalechildbearingage=patients.satisfying(
            """
            (age <=55) AND
            (sex = 'F')
            """,
    ),
    teratogenicmeds_last12m=patients.satisfying(
        """
       teratogenicmeds_issuecount >=2 AND
       femalechildbearingage
       """,    
        teratogenicmeds_issuecount=patients.with_these_medications(
            teratogenic_codes,
            between=["last_day_of_month(index_date) - 365 days", "last_day_of_month(index_date)"],
            returning='number_of_matches_in_period',
            return_expectations={"incidence": 0.3},
        ),
    ),

    dmards_last12m=patients.satisfying(
        """
       dmard_codes_issuecount >=2
       """,    
        dmard_codes_issuecount=patients.with_these_medications(
            dmard_codes,
            between=["last_day_of_month(index_date) - 365 days", "last_day_of_month(index_date)"],
            returning='number_of_matches_in_period',
            return_expectations={"incidence": 0.3},
        ),
    ),

    addictivemeds_last12m=patients.satisfying(
        """
       addictive_issuecount >=2
       """,    
        addictive_issuecount=patients.with_these_medications(
            combined_addictive_codes,
            between=["last_day_of_month(index_date) - 365 days", "last_day_of_month(index_date)"],
            returning='number_of_matches_in_period',
            return_expectations={"incidence": 0.3},
        ),
    ),

    highriskmeds_last12m=patients.satisfying(
        """
        teratogenicmeds_last12m OR
        dmards_last12m OR
        addictivemeds_last12m
        """,
    ), 
)