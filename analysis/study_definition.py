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
    registered=patients.registered_as_of("index_date"),
    # Or should this be registered with one practice?
    died=patients.died_from_any_cause(
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.1},
    ),
)
