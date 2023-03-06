from cohortextractor import StudyDefinition, patients, Measure, params, codelist_from_csv
from report.populations import population_filters
from report.demographics import demographics
from report.event_variables import generate_event_variables
from report.report_utils import calculate_variable_windows

codelist_1_path = params["codelist_1_path"]
codelist_1_column = params["codelist_1_column"]
codelist_1_system = params["codelist_1_system"]
codelist_1_type = params["codelist_1_type"]
population_definition = params["population"]
time_window = params["time_window"]

codelist_1 = codelist_from_csv(
    codelist_1_path,
    system=codelist_1_system,
    column=codelist_1_column,
)


selected_population = population_filters[population_definition]

medication_review_variables = {}

if time_window == "ever":
    medication_review_variables["medication_review"] = patients.with_these_clinical_events(
        codelist_1,
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={
            "incidence": 0.5,
        },
    )

else:
    medication_review_variables["medication_review"] = patients.with_these_clinical_events(
        codelist_1,
        between=[f"index_date - {time_window}", "index_date"],
        returning="binary_flag",
        return_expectations={
            "incidence": 0.5,
        },
    )


study = StudyDefinition(
    index_date="2019-01-01",
    default_expectations={
        "date": {"earliest": "2020-01-01", "latest": "2022-12-01"},
        "rate": "exponential_increase",
        "incidence": 0.1,
    },
    population=selected_population,
    age=patients.age_as_of(
        "index_date",
        return_expectations={
            "rate": "universal",
            "int": {"distribution": "population_ages"},
        },
    ),
    practice=patients.registered_practice_as_of(
        "index_date",
        returning="pseudo_id",
        return_expectations={
            "int": {"distribution": "normal", "mean": 25, "stddev": 5},
            "incidence": 0.5,
        },
    ),

    **medication_review_variables

   
)
