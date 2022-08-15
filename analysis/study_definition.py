from cohortextractor import StudyDefinition, patients, codelist, codelist_from_csv, Measure  # NOQA

from codelists import *
from common_variables import common_variables

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
    had_smr=patients.with_these_clinical_events(
            smr_codes,
            between =["last_day_of_month(index_date) - 365 days", "last_day_of_month(index_date)"],
            returning='binary_flag',
            return_expectations={"incidence": 0.2}
    ),
)

measures = [
    Measure(
        id="smr_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["population"],
        small_number_suppression=True,
    ),
    Measure(
        id="smr_age_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["age_band"],
        small_number_suppression=True,
    ),
    Measure(
        id="smr_sex_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["sex"],
        small_number_suppression=True,
    ),
    Measure(
        id="smr_imdQ5_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["imdQ5"],
        small_number_suppression=True,
    ),   
]
