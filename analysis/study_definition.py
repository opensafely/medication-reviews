from cohortextractor import StudyDefinition, patients, codelist, codelist_from_csv, Measure  # NOQA

from codelists import *
from common_variables import common_variables
from utilities import loop_over_codes

start_date = "2019-04-01"
end_date = "2022-03-01"

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
       (age >=18 AND age <=120) AND
       NOT died AND
       (sex = 'M' OR sex = 'F')
       """,
        registered=patients.registered_as_of("last_day_of_month(index_date)"),
        died=patients.died_from_any_cause(
            on_or_before="last_day_of_month(index_date)",
            returning="binary_flag",
            return_expectations={"incidence": 0.1},
        ),
    ),
    **common_variables,
    **loop_over_codes(med_review_codes),
)

measures = [
    ## SMR codelist measures
    Measure(
        id="smr_population_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["population"],
    ),
    Measure(
        id="smr_practice_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["practice"],
    ),
    Measure(
        id="smr_age_band_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["age_band"],
    ),
    Measure(
        id="smr_sex_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["sex"],
    ),
    Measure(
        id="smr_imdQ5_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["imdQ5"],
    ),
    Measure(
        id="smr_region_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["region"],
    ),
    Measure(
        id="smr_ethnicity_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["ethnicity"],
    ),
    Measure(
        id="smr_learning_disability_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["learning_disability"],
    ),
    Measure(
        id="smr_nhome_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["nhome"],
    ),
    Measure(
        id="smr_care_home_type_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["care_home_type"],
    ),
    ## Medication review codelist measures
    Measure(
        id="mr_population_rate",
        numerator="had_mr",
        denominator="population",
        group_by=["population"],
    ),
    Measure(
        id="mr_practice_rate",
        numerator="had_mr",
        denominator="population",
        group_by=["practice"],
    ),
    Measure(
        id="mr_age_band_rate",
        numerator="had_mr",
        denominator="population",
        group_by=["age_band"],
    ),
    Measure(
        id="mr_sex_rate",
        numerator="had_mr",
        denominator="population",
        group_by=["sex"],
    ),
    Measure(
        id="mr_imdQ5_rate",
        numerator="had_mr",
        denominator="population",
        group_by=["imdQ5"],
    ),
    Measure(
        id="mr_region_rate",
        numerator="had_mr",
        denominator="population",
        group_by=["region"],
    ),
    Measure(
        id="mr_ethnicity_rate",
        numerator="had_mr",
        denominator="population",
        group_by=["ethnicity"],
    ),
    Measure(
        id="mr_learning_disability_rate",
        numerator="had_mr",
        denominator="population",
        group_by=["learning_disability"],
    ),
    Measure(
        id="mr_nhome_rate",
        numerator="had_mr",
        denominator="population",
        group_by=["nhome"],
    ),
    Measure(
        id="mr_care_home_type_rate",
        numerator="had_mr",
        denominator="population",
        group_by=["care_home_type"],
    ),
]
