from cohortextractor import (
    codelist_from_csv,
)

# COVARIATES

ethnicity_codes = codelist_from_csv(
    "codelists/opensafely-ethnicity-snomed-0removed.csv",
    system="snomed",
    column="snomedcode",
    category_column="Grouping_6",
)

learning_disability_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-ld_cod.csv",
    system="snomed",
    column="code",
)

smr_codes = codelist_from_csv(
    "codelists/opensafely-structured-medication-review-nhs-england.csv",
    system="snomed",
    column="code",
)

nhse_care_homes_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-carehome_cod.csv",
    system="snomed",
    column="code",
)

med_review_codes = codelist_from_csv(
    "codelists/user-chriswood-medication-review.csv",
    system="snomed",
    column="code",
)
