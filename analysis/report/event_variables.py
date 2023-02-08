from cohortextractor import patients
from utilities import generate_expectations_codes

def clinical_event(codelist, date_range, event_name):
    events = {
        f"{event_name}": (patients.with_these_clinical_events(
            codelist=codelist,
            between=date_range,
            returning="binary_flag",
            return_expectations={"incidence": 0.5},
        )),
        f"{event_name}_code": (patients.with_these_clinical_events(
            codelist=codelist,
            between=date_range,
            returning="code",
            return_expectations={
                "rate": "universal",
                "category": {"ratios": generate_expectations_codes(codelist)},
            },
        )),
        f"{event_name}_date": (patients.with_these_clinical_events(
            codelist=codelist,
            between=date_range,
            returning="date",
            date_format="YYYY-MM-DD",
            return_expectations={
                "date": {
                    "earliest": "index_date",
                    "latest": "last_day_of_month(index_date)",
                }
            },
        )),
    }

    return events

def medication_event(codelist, date_range, event_name):
    events = {
        f"{event_name}": (patients.with_these_medications(
            codelist=codelist,
            between=date_range,
            returning="binary_flag",
            return_expectations={"incidence": 0.5},
        )),
        f"{event_name}_code": (patients.with_these_medications(
            codelist=codelist,
            between=date_range,
            returning="code",
            return_expectations={
                "rate": "universal",
                "category": {"ratios": generate_expectations_codes(codelist)},
            },
        )),
        f"{event_name}_date": (patients.with_these_medications(
            codelist=codelist,
            between=date_range,
            returning="date",
            date_format="YYYY-MM-DD",
            return_expectations={
                "date": {
                    "earliest": "index_date",
                    "latest": "last_day_of_month(index_date)",
                }
            },
        )),

    }

    return events


def generate_event_variables(codelist_1_type, codelist_1, codelist_1_date_range, codelist_2_type, codelist_2, codelist_2_date_range):

    if codelist_1_type == "clinical":
        event_1 = clinical_event(codelist_1, codelist_1_date_range, "event_1")
    else:
        event_1 = medication_event(codelist_1, codelist_1_date_range, "event_1")
   
    if codelist_2_type == "clinical":
        event_2 = clinical_event(codelist_2, codelist_2_date_range, "event_2")
    else:
        event_2 = medication_event(codelist_2, codelist_2_date_range, "event_2")

    measure_variable = {
        "event_measure": (patients.satisfying(
            f"""
            event_1 = 1 AND event_2 = 1
            """,
            return_expectations={"incidence": 0.5},
        )),
            
    }

    return {**event_1, **event_2, **measure_variable}