from cohortextractor import StudyDefinition, patients, Measure, params, codelist_from_csv
from utilities import generate_expectations_codes
from report.populations import population_filters
from report.demographics import demographics
from report.report_utils import calculate_variable_windows

codelist_1_path = params["codelist_1_path"]
codelist_1_column = params["codelist_1_column"]
codelist_1_system = params["codelist_1_system"]
codelist_2_path = params["codelist_2_path"]
codelist_2_column = params["codelist_2_column"]
codelist_2_system = params["codelist_2_system"]
codelist_2_period_start = params["codelist_2_period_start"]
codelist_2_period_end = params["codelist_2_period_end"]
operator = params["operator"]
codelist_2_comparison_date = params["codelist_2_comparison_date"]
codelist_1_frequency = params["codelist_1_frequency"]
population_definition = params["population"]
breakdowns = [x for x in params["breakdowns"].split(",")]

codelist_1 = codelist_from_csv(
    codelist_1_path,
    system=codelist_1_system,
    column=codelist_1_column,
)

codelist_2 = codelist_from_csv(
    codelist_2_path,
    system=codelist_2_system,
    column=codelist_2_column,
)

codelist_1 = codelist_from_csv(
    "codelists/user-chriswood-all-medication-reviews.csv",
    system="snomed",
    column="code",
)

codelist_2 = codelist_from_csv(
    "codelists/opensafely-dmards.csv",
    system="snomed",
    column="snomed_id",
)


codelist_1_date_range, codelist_2_date_range = calculate_variable_windows(
    codelist_1_frequency,
    codelist_2_comparison_date,
    codelist_2_period_start,
    codelist_2_period_end,
)
selected_population = population_filters[population_definition]
selected_demographics = {k: v for k, v in demographics.items() if k in breakdowns}

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
    **selected_demographics,
    practice=patients.registered_practice_as_of(
        "index_date",
        returning="pseudo_id",
        return_expectations={
            "int": {"distribution": "normal", "mean": 25, "stddev": 5},
            "incidence": 0.5,
        },
    ),
    event_1=patients.with_these_clinical_events(
        codelist=codelist_1,
        between=codelist_1_date_range,
        returning="binary_flag",
        return_expectations={"incidence": 0.5},
    ),
    event_1_code=patients.with_these_clinical_events(
        codelist=codelist_1,
        between=codelist_1_date_range,
        returning="code",
        return_expectations={
            "rate": "universal",
            "category": {"ratios": generate_expectations_codes(codelist_1)},
        },
    ),
    event_1_date=patients.with_these_clinical_events(
        codelist=codelist_1,
        between=codelist_1_date_range,
        returning="date",
        date_format="YYYY-MM-DD",
        return_expectations={
            "date": {
                "earliest": "index_date",
                "latest": "last_day_of_month(index_date)",
            }
        },
    ),
    event_2=patients.with_these_medications(
        codelist=codelist_2,
        between=codelist_2_date_range,
        returning="binary_flag",
        return_expectations={"incidence": 0.5},
    ),
    event_2_code=patients.with_these_medications(
        codelist=codelist_2,
        between=codelist_2_date_range,
        returning="code",
        return_expectations={
            "rate": "universal",
            "category": {"ratios": generate_expectations_codes(codelist_2)},
        },
    ),
    event_2_date=patients.with_these_medications(
        codelist=codelist_2,
        between=codelist_2_date_range,
        returning="date",
        return_expectations={
            "date": {
                "earliest": "index_date",
                "latest": "last_day_of_month(index_date)",
            }
        },
    ),
    event_measure=patients.satisfying(
        f"""
        event_1 = 1 {operator} event_2 = 1
        """,
        return_expectations={"incidence": 0.5},
    ),
)

measures = [
    Measure(
        id=f"event_rate",
        numerator="event_measure",
        denominator="population",
        group_by=["practice"],
    ),
    Measure(
        id=f"event_code_1_rate",
        numerator="event_measure",
        denominator="population",
        group_by=["event_1_code"],
    ),
    Measure(
        id=f"event_code_2_rate",
        numerator="event_measure",
        denominator="population",
        group_by=["event_2_code"],
    ),
]

if breakdowns:
    for b in breakdowns:
        measures.append(
            Measure(
                id=f"event_{b}_rate",
                numerator="event_measure",
                denominator="population",
                group_by=[b],
            ),
        )
