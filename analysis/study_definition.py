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
)
