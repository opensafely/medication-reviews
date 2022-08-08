from cohortextractor import StudyDefinition, patients, codelist, codelist_from_csv  # NOQA

start_date = "2019-02-01"
end_date = "2020-02-01"

study = StudyDefinition(
    index_date=start_date,
    default_expectations={
        "date": {"earliest": start_date, "latest": end_date},
        "rate": "uniform",
        "incidence": 0.5,
    },
    population=patients.satisfying(
        """
       registered AND
       NOT died AND
       (age >=18 AND age <=120) AND
       (sex = 'M' OR sex = 'F')
       """
    ),
    registered=patients.registered_practice_as_of(
        "index_date",
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
                    "London": 0.2,
                    "South East": 0.1,
                    "South West": 0.1,
                },
            },
        },
    ),
    # Or should this be registered with one practice?
    died=patients.died_from_any_cause(
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.1},
    ),
    age=patients.age_as_of(
        "index_date",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),
    age_band=patients.categorised_as(
        {
            "missing": "DEFAULT",
            "0-19": """ age >= 0 AND age < 20""",
            "20-29": """ age >=  20 AND age < 30""",
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
                    "0-19": 0.035,
                    "20-29": 0.12,
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
            "index_date",
            returning="index_of_multiple_deprivation",
            round_to_nearest=100,
        )
    ),
)
