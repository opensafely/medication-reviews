from cohortextractor import StudyDefinition, patients, codelist, codelist_from_csv, Measure  # NOQA

from codelists import *
from common_variables import common_variables
from study_definition_utilities import loop_over_codes

start_date = "2019-04-01"
end_date = "2022-03-01"

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
       NOT died AND
       (sex = 'M' OR sex = 'F')
       """,
        registered=patients.registered_as_of("last_day_of_month(index_date)"),
        died=patients.died_from_any_cause(
            on_or_before="last_day_of_month(index_date)",
            returning="binary_flag",
            return_expectations={"incidence": 0.1},
        ),
    ),
    had_smr=patients.with_these_clinical_events(
        smr_codes,
        between=["first_day_of_month(index_date)", "last_day_of_month(index_date)"],
        returning='binary_flag',
        return_expectations={"incidence": 0.3},
    ),
    had_smr12m=patients.with_these_clinical_events(
        smr_codes,
        between =["last_day_of_month(index_date) - 365 days", "last_day_of_month(index_date)"],
        returning='binary_flag',
        return_expectations={"incidence": 0.2},
    ),
    had_mr=patients.with_these_clinical_events(
        med_review_codes,
        between =["first_day_of_month(index_date)", "last_day_of_month(index_date)"],
        returning='binary_flag',
        return_expectations={"incidence": 0.3},
    ),
    had_mr12m=patients.with_these_clinical_events(
        med_review_codes,
        between =["last_day_of_month(index_date) - 365 days", "last_day_of_month(index_date)"],
        returning='binary_flag',
        return_expectations={"incidence": 0.3},
    ),
    **common_variables,
    **loop_over_codes(med_review_codes),
)

measures = [
    ## SMR codelist measures
    Measure(
        id="smr_population_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["population"],
    ),
    Measure(
        id="smr_practice_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["practice"],
    ),
    Measure(
        id="smr_age_band_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["age_band"],
    ),
    Measure(
        id="smr_sex_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["sex"],
    ),
    Measure(
        id="smr_imdQ5_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["imdQ5"],
    ),
    Measure(
        id="smr_region_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["region"],
    ),
    Measure(
        id="smr_ethnicity_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["ethnicity"],
    ),
    Measure(
        id="smr_ethnicity16_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["ethnicity16"],
    ),
    Measure(
        id="smr_learning_disability_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["learning_disability"],
    ),
    Measure(
        id="smr_nhome_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["nhome"],
    ),
    Measure(
        id="smr_care_home_type_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["care_home_type"],
    ),
    Measure(
        id="smr_teratogenic_meds_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["teratogenicmeds_last12m"],
    ),
    Measure(
        id="smr_dmards_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["dmards_last12m"],
    ),
    Measure(
        id="smr_addictive_meds_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["addictivemeds_last12m"],
    ),
    Measure(
        id="smr_highrisk_meds_rate",
        numerator="had_smr",
        denominator="population",
        group_by=["highriskmeds_last12m"],
    ),
    ## SMR in last 12m measures
    Measure(
        id="smr12m_population_rate",
        numerator="had_smr12m",
        denominator="population",
        group_by=["population"],
    ),
    Measure(
        id="smr12m_practice_rate",
        numerator="had_smr12m",
        denominator="population",
        group_by=["practice"],
    ),
    Measure(
        id="smr12m_age_band_rate",
        numerator="had_smr12m",
        denominator="population",
        group_by=["age_band"],
    ),
    Measure(
        id="smr12m_sex_rate",
        numerator="had_smr12m",
        denominator="population",
        group_by=["sex"],
    ),
    Measure(
        id="smr12m_imdQ5_rate",
        numerator="had_smr12m",
        denominator="population",
        group_by=["imdQ5"],
    ),
    Measure(
        id="smr12m_region_rate",
        numerator="had_smr12m",
        denominator="population",
        group_by=["region"],
    ),
    Measure(
        id="smr12m_ethnicity_rate",
        numerator="had_smr12m",
        denominator="population",
        group_by=["ethnicity"],
    ),
    Measure(
        id="smr12m_ethnicity16_rate",
        numerator="had_smr12m",
        denominator="population",
        group_by=["ethnicity16"],
    ),
    Measure(
        id="smr12m_learning_disability_rate",
        numerator="had_smr12m",
        denominator="population",
        group_by=["learning_disability"],
    ),
    Measure(
        id="smr12m_nhome_rate",
        numerator="had_smr12m",
        denominator="population",
        group_by=["nhome"],
    ),
    Measure(
        id="smr12m_care_home_type_rate",
        numerator="had_smr12m",
        denominator="population",
        group_by=["care_home_type"],
    ),
    Measure(
        id="smr12m_teratogenic_meds_rate",
        numerator="had_smr12m",
        denominator="population",
        group_by=["teratogenicmeds_last12m"],
    ),
    Measure(
        id="smr12m_dmards_rate",
        numerator="had_smr12m",
        denominator="population",
        group_by=["dmards_last12m"],
    ),
    Measure(
        id="smr12m_addictive_meds_rate",
        numerator="had_smr12m",
        denominator="population",
        group_by=["addictivemeds_last12m"],
    ),
    Measure(
        id="smr12m_highrisk_meds_rate",
        numerator="had_smr12m",
        denominator="population",
        group_by=["highriskmeds_last12m"],
    ),
    ## Medication review codelist measures
    Measure(
        id="mr_population_rate",
        numerator="had_mr",
        denominator="population",
        group_by=["population"],
    ),
    Measure(
        id="mr_practice_rate",
        numerator="had_mr",
        denominator="population",
        group_by=["practice"],
    ),
    Measure(
        id="mr_age_band_rate",
        numerator="had_mr",
        denominator="population",
        group_by=["age_band"],
    ),
    Measure(
        id="mr_sex_rate",
        numerator="had_mr",
        denominator="population",
        group_by=["sex"],
    ),
    Measure(
        id="mr_imdQ5_rate",
        numerator="had_mr",
        denominator="population",
        group_by=["imdQ5"],
    ),
    Measure(
        id="mr_region_rate",
        numerator="had_mr",
        denominator="population",
        group_by=["region"],
    ),
    Measure(
        id="mr_ethnicity_rate",
        numerator="had_mr",
        denominator="population",
        group_by=["ethnicity"],
    ),
    Measure(
        id="mr_learning_disability_rate",
        numerator="had_mr",
        denominator="population",
        group_by=["learning_disability"],
    ),
    Measure(
        id="mr_nhome_rate",
        numerator="had_mr",
        denominator="population",
        group_by=["nhome"],
    ),
    Measure(
        id="mr_care_home_type_rate",
        numerator="had_mr",
        denominator="population",
        group_by=["care_home_type"],
    ),
    Measure(
        id="mr_teratogenic_meds_rate",
        numerator="had_mr",
        denominator="population",
        group_by=["teratogenicmeds_last12m"],
    ),
    Measure(
        id="mr_dmards_rate",
        numerator="had_mr",
        denominator="population",
        group_by=["dmards_last12m"],
    ),
    Measure(
        id="mr_addictive_meds_rate",
        numerator="had_mr",
        denominator="population",
        group_by=["addictivemeds_last12m"],
    ),
    Measure(
        id="mr_highrisk_meds_rate",
        numerator="had_mr",
        denominator="population",
        group_by=["highriskmeds_last12m"],
    ),
    ## MR in last 12m measures
    Measure(
        id="mr12m_population_rate",
        numerator="had_mr12m",
        denominator="population",
        group_by=["population"],
    ),
    Measure(
        id="mr12m_practice_rate",
        numerator="had_mr12m",
        denominator="population",
        group_by=["practice"],
    ),
    Measure(
        id="mr12m_age_band_rate",
        numerator="had_mr12m",
        denominator="population",
        group_by=["age_band"],
    ),
    Measure(
        id="mr12m_sex_rate",
        numerator="had_mr12m",
        denominator="population",
        group_by=["sex"],
    ),
    Measure(
        id="mr12m_imdQ5_rate",
        numerator="had_mr12m",
        denominator="population",
        group_by=["imdQ5"],
    ),
    Measure(
        id="mr12m_region_rate",
        numerator="had_mr12m",
        denominator="population",
        group_by=["region"],
    ),
    Measure(
        id="mr12m_ethnicity_rate",
        numerator="had_mr12m",
        denominator="population",
        group_by=["ethnicity"],
    ),
    Measure(
        id="mr12m_learning_disability_rate",
        numerator="had_mr12m",
        denominator="population",
        group_by=["learning_disability"],
    ),
    Measure(
        id="mr12m_nhome_rate",
        numerator="had_mr12m",
        denominator="population",
        group_by=["nhome"],
    ),
    Measure(
        id="mr12m_care_home_type_rate",
        numerator="had_mr12m",
        denominator="population",
        group_by=["care_home_type"],
    ),
    Measure(
        id="mr12m_teratogenic_meds_rate",
        numerator="had_mr12m",
        denominator="population",
        group_by=["teratogenicmeds_last12m"],
    ),
    Measure(
        id="mr12m_dmards_rate",
        numerator="had_mr12m",
        denominator="population",
        group_by=["dmards_last12m"],
    ),
    Measure(
        id="mr12m_addictive_meds_rate",
        numerator="had_mr12m",
        denominator="population",
        group_by=["addictivemeds_last12m"],
    ),
    Measure(
        id="mr12m_highrisk_meds_rate",
        numerator="had_mr12m",
        denominator="population",
        group_by=["highriskmeds_last12m"],
    ),

    ##Age-sex grouped for standardisation
    ## SMR codelist measures
    Measure(
        id="smr_population_rate_agesexstandardgrouped",
        numerator="had_smr",
        denominator="population",
        group_by=["AgeGroup", "sex"],
    ),
    Measure(
        id="smr_practice_rate_agesexstandardgrouped",
        numerator="had_smr",
        denominator="population",
        group_by=["AgeGroup", "sex", "practice"],
    ),
    Measure(
        id="smr_age_band_rate_agesexstandardgrouped",
        numerator="had_smr",
        denominator="population",
        group_by=["sex", "age_band"],
    ),
    Measure(
        id="smr_sex_rate_agesexstandardgrouped",
        numerator="had_smr",
        denominator="population",
        group_by=["AgeGroup", "sex"],
    ),
    Measure(
        id="smr_imdQ5_rate_agesexstandardgrouped",
        numerator="had_smr",
        denominator="population",
        group_by=["AgeGroup", "sex", "imdQ5"],
    ),
    Measure(
        id="smr_region_rate_agesexstandardgrouped",
        numerator="had_smr",
        denominator="population",
        group_by=["AgeGroup", "sex", "region"],
    ),
    Measure(
        id="smr_ethnicity_rate_agesexstandardgrouped",
        numerator="had_smr",
        denominator="population",
        group_by=["AgeGroup", "sex", "ethnicity"],
    ),
    Measure(
        id="smr_ethnicity16_rate_agesexstandardgrouped",
        numerator="had_smr",
        denominator="population",
        group_by=["AgeGroup", "sex", "ethnicity16"],
    ),
    Measure(
        id="smr_learning_disability_rate_agesexstandardgrouped",
        numerator="had_smr",
        denominator="population",
        group_by=["AgeGroup", "sex", "learning_disability"],
    ),
    Measure(
        id="smr_nhome_rate_agesexstandardgrouped",
        numerator="had_smr",
        denominator="population",
        group_by=["AgeGroup", "sex", "nhome"],
    ),
    Measure(
        id="smr_care_home_type_rate_agesexstandardgrouped",
        numerator="had_smr",
        denominator="population",
        group_by=["AgeGroup", "sex", "care_home_type"],
    ),
    Measure(
        id="smr_teratogenic_meds_rate_agesexstandardgrouped",
        numerator="had_smr",
        denominator="population",
        group_by=["AgeGroup", "sex", "teratogenicmeds_last12m"],
    ),
    Measure(
        id="smr_dmards_rate_agesexstandardgrouped",
        numerator="had_smr",
        denominator="population",
        group_by=["AgeGroup", "sex", "dmards_last12m"],
    ),
    Measure(
        id="smr_addictive_meds_rate_agesexstandardgrouped",
        numerator="had_smr",
        denominator="population",
        group_by=["AgeGroup", "sex", "addictivemeds_last12m"],
    ),
    Measure(
        id="smr_highrisk_meds_rate_agesexstandardgrouped",
        numerator="had_smr",
        denominator="population",
        group_by=["AgeGroup", "sex", "highriskmeds_last12m"],
    ),
    ## SMR in last 12m measures
    Measure(
        id="smr12m_population_rate_agesexstandardgrouped",
        numerator="had_smr12m",
        denominator="population",
        group_by=["AgeGroup", "sex"],
    ),
    Measure(
        id="smr12m_practice_rate_agesexstandardgrouped",
        numerator="had_smr12m",
        denominator="population",
        group_by=["AgeGroup", "sex", "practice"],
    ),
    Measure(
        id="smr12m_age_band_rate_agesexstandardgrouped",
        numerator="had_smr12m",
        denominator="population",
        group_by=["sex", "age_band"],
    ),
    Measure(
        id="smr12m_sex_rate_agesexstandardgrouped",
        numerator="had_smr12m",
        denominator="population",
        group_by=["AgeGroup", "sex"],
    ),
    Measure(
        id="smr12m_imdQ5_rate_agesexstandardgrouped",
        numerator="had_smr12m",
        denominator="population",
        group_by=["AgeGroup", "sex", "imdQ5"],
    ),
    Measure(
        id="smr12m_region_rate_agesexstandardgrouped",
        numerator="had_smr12m",
        denominator="population",
        group_by=["AgeGroup", "sex", "region"],
    ),
    Measure(
        id="smr12m_ethnicity_rate_agesexstandardgrouped",
        numerator="had_smr12m",
        denominator="population",
        group_by=["AgeGroup", "sex", "ethnicity"],
    ),
    Measure(
        id="smr12m_ethnicity16_rate_agesexstandardgrouped",
        numerator="had_smr12m",
        denominator="population",
        group_by=["AgeGroup", "sex", "ethnicity16"],
    ),
    Measure(
        id="smr12m_learning_disability_rate_agesexstandardgrouped",
        numerator="had_smr12m",
        denominator="population",
        group_by=["AgeGroup", "sex", "learning_disability"],
    ),
    Measure(
        id="smr12m_nhome_rate_agesexstandardgrouped",
        numerator="had_smr12m",
        denominator="population",
        group_by=["AgeGroup", "sex", "nhome"],
    ),
    Measure(
        id="smr12m_care_home_type_rate_agesexstandardgrouped",
        numerator="had_smr12m",
        denominator="population",
        group_by=["AgeGroup", "sex", "care_home_type"],
    ),
    Measure(
        id="smr12m_teratogenic_meds_rate_agesexstandardgrouped",
        numerator="had_smr12m",
        denominator="population",
        group_by=["AgeGroup", "sex", "teratogenicmeds_last12m"],
    ),
    Measure(
        id="smr12m_dmards_rate_agesexstandardgrouped",
        numerator="had_smr12m",
        denominator="population",
        group_by=["AgeGroup", "sex", "dmards_last12m"],
    ),
    Measure(
        id="smr12m_addictive_meds_rate_agesexstandardgrouped",
        numerator="had_smr12m",
        denominator="population",
        group_by=["AgeGroup", "sex", "addictivemeds_last12m"],
    ),
    Measure(
        id="smr12m_highrisk_meds_rate_agesexstandardgrouped",
        numerator="had_smr12m",
        denominator="population",
        group_by=["AgeGroup", "sex", "highriskmeds_last12m"],
    ),
]
