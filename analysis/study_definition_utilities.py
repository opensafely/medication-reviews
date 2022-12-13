
from cohortextractor import patients, codelist

def loop_over_codes(code_list):
    def make_variable(code):
        return {
            f"count_{code}": (
                patients.with_these_clinical_events(
                    codelist([code], system="snomed"),
                    between =["first_day_of_month(index_date)", "last_day_of_month(index_date)"],
                    returning="number_of_matches_in_period",
                    return_expectations={
                         "incidence": 0.1,
                         "int": {"distribution": "normal", "mean": 3, "stddev": 1},
                    },
                )
            )
        }

    variables = {}
    for code in code_list:
        variables.update(make_variable(code))
    return variables