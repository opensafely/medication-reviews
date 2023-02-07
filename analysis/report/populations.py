
from cohortextractor import patients

population_filters = {
    "registered_adults": (patients.satisfying(
        """
        registered AND
        NOT died AND
        age >= 18 AND
        age <= 120
        """,

        registered = patients.registered_as_of(
            "index_date",
            return_expectations={"incidence": 0.9},
            ),

        died = patients.died_from_any_cause(
            on_or_before="index_date",
            returning="binary_flag",
            return_expectations={"incidence": 0.1}
            ),
        
    )),
    "registered_children": (patients.satisfying(
        """
        registered AND
        NOT died AND
        age < 18
        """,

        registered = patients.registered_as_of(
            "index_date",
            return_expectations={"incidence": 0.9},
            ),

        died = patients.died_from_any_cause(
            on_or_before="index_date",
            returning="binary_flag",
            return_expectations={"incidence": 0.1}
            ),
        
    )),
    "all_registered": (patients.satisfying(
        """
        registered AND
        NOT died
        """,

        registered = patients.registered_as_of(
        "index_date",
        return_expectations={"incidence": 0.9},
        ),

        died = patients.died_from_any_cause(
        on_or_before="index_date",
        returning="binary_flag",
        return_expectations={"incidence": 0.1}
        ),
    )),
}