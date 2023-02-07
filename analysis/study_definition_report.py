from cohortextractor import (
    StudyDefinition,
    patients,
    Measure,
    params
)
from codelists import *
from utilities import generate_expectations_codes
from report.populations import population_filters
from report.demographics import demographics

codelist_1 = allmed_review_codes
codelist_2 = dmard_codes



codelist_2_period_start = params["codelist_2_period_start"]
codelist_2_period_end = params["codelist_2_period_end"]
operator = params["operator"]
codelist_2_comparison_date = params["codelist_2_comparison_date"]
codelist_1_frequency = params["codelist_1_frequency"]
population_definition = params["population"]
breakdowns = [x for x in params["breakdowns"].split(",")]


# codelist 1 frequency
if codelist_1_frequency == "weekly":
    codelist_1_date_range = ["index_date", "index_date + 7 days"]
elif codelist_1_frequency == "monthly":
    codelist_1_date_range = ["index_date", "last_day_of_month(index_date"]


#codelist 2 date range
if codelist_2_comparison_date == "start_date":
    codelist_2_date_range = [f"index_date {codelist_2_period_start} days", f"index_date {codelist_2_period_end} days"]
elif codelist_2_comparison_date == "end_date":
    codelist_2_date_range = [f"{codelist_1_date_range[1]} {codelist_2_period_start} days", f"{codelist_1_date_range[1]} {codelist_2_period_end} days"]
elif codelist_2_comparison_date == "event_1_date":
    codelist_2_date_range = [f"event_1_date {codelist_2_period_start} days", f"event_1_date {codelist_2_period_end} days"]


# Specifiy study definition


selected_population = population_filters[population_definition]
selected_demographics = {k: v for k, v in demographics.items() if k in breakdowns}

study = StudyDefinition(
    index_date="2019-01-01",
    default_expectations={
        "date": {"earliest": "2020-01-01", "latest": "2022-12-01"},
        "rate": "exponential_increase",
        "incidence": 0.1,
    },
    
    population= selected_population,
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
        return_expectations={"int" : {"distribution": "normal", "mean": 25, "stddev": 5}, "incidence" : 0.5}
    ),
      
    event_1=patients.with_these_clinical_events(
        codelist=codelist_1,
        between=codelist_1_date_range,
        returning="binary_flag",
        return_expectations={"incidence": 0.5}
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

    event_1_date = patients.with_these_clinical_events(
        codelist=codelist_1,
        between=codelist_1_date_range,
        returning="date",
        date_format="YYYY-MM-DD",
        return_expectations={"date": {"earliest": "index_date", "latest": "last_day_of_month(index_date)"}},
    ),

    event_2=patients.with_these_medications(
        codelist=codelist_2,
        between=codelist_2_date_range,
        returning="binary_flag",
        return_expectations={"incidence": 0.5}
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

    event_2_date = patients.with_these_medications(
        codelist=codelist_2,
        between=codelist_2_date_range,
        returning="date",
        return_expectations={"date": {"earliest": "index_date", "latest": "last_day_of_month(index_date)"}},
    ),

    event_measure = patients.satisfying(
        f"""
        event_1 = 1 {operator} event_2 = 1
        """,
        return_expectations={"incidence": 0.5}
    ),


    
    
   
)

measures = [
    Measure(
        id=f"event_rate",
        numerator="event_measure",
        denominator="population",
        group_by=["practice"]
    ),
    Measure(
        id=f"event_code_1_rate",
        numerator="event_measure",
        denominator="population",
        group_by=["event_1_code"]
    ),
    Measure(
        id=f"event_code_2_rate",
        numerator="event_measure",
        denominator="population",
        group_by=["event_2_code"]
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


   