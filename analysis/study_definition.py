from cohortextractor import StudyDefinition, patients, codelist, codelist_from_csv  # NOQA

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
       (age_band != "missing") AND
       (imd != -1) AND
       NOT died AND
       (sex = 'M' OR sex = 'F')
       """
    ),
    **common_variables,
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
            "PC":
            """
            IsPotentialCareHome
            AND LocationDoesNotRequireNursing='Y'
            AND LocationRequiresNursing='N'
            """,
            "PN":
            """
            IsPotentialCareHome
            AND LocationDoesNotRequireNursing='N'
            AND LocationRequiresNursing='Y'
            """,
            "PS": "IsPotentialCareHome",
            "PR": "NOT IsPotentialCareHome",
            "": "DEFAULT",
        },
        return_expectations={
            "rate": "universal",
            "category": {"ratios": {"PC": 0.05, "PN": 0.05, "PS": 0.05, "PR": 0.84, "": 0.01},},
        },
    ),
)
