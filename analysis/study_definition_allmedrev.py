from cohortextractor import StudyDefinition, patients, combine_codelists, codelist, codelist_from_csv, Measure  # NOQA

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
    **common_variables,
    
    had_anymedrev=patients.with_these_clinical_events(
        allmed_review_codes,
        between=["first_day_of_month(index_date)", "last_day_of_month(index_date)"],
        returning='binary_flag',
        return_expectations={"incidence": 0.3},
    ),
    had_anymedrev12m=patients.with_these_clinical_events(
        allmed_review_codes,
        between =["last_day_of_month(index_date) - 365 days", "last_day_of_month(index_date)"],
        returning='binary_flag',
        return_expectations={"incidence": 0.3},
    ),
    **loop_over_codes(allmed_review_codes),
)

measures = [
    Measure(
        id="allmedrv_population_rate",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["population"],
    ),
    Measure(
        id="allmedrv_practice_rate",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["practice"],
    ),
    Measure(
        id="allmedrv_age_band_rate",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["age_band"],
    ),
    Measure(
        id="allmedrv_sex_rate",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["sex"],
    ),
    Measure(
        id="allmedrv_imdQ5_rate",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["imdQ5"],
    ),
    Measure(
        id="allmedrv_region_rate",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["region"],
    ),
    Measure(
        id="allmedrv_ethnicity_rate",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["ethnicity"],
    ),
    Measure(
        id="allmedrv_ethnicity16_rate",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["ethnicity16"],
    ),
    Measure(
        id="allmedrv_learning_disability_rate",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["learning_disability"],
    ),
    Measure(
        id="allmedrv_nhome_rate",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["nhome"],
    ),
    Measure(
        id="allmedrv_care_home_type_rate",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["care_home_type"],
    ),
    Measure(
        id="allmedrv_teratogenic_meds_rate",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["teratogenicmeds_last12m"],
    ),
    Measure(
        id="allmedrv_dmards_rate",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["dmards_last12m"],
    ),
    Measure(
        id="allmedrv_addictive_meds_rate",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["addictivemeds_last12m"],
    ),
    Measure(
        id="allmedrv_highrisk_meds_rate",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["highriskmeds_last12m"],
    ),
    Measure(
        id="allmedrv12m_population_rate",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["population"],
    ),
    Measure(
        id="allmedrv12m_practice_rate",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["practice"],
    ),
    Measure(
        id="allmedrv12m_age_band_rate",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["age_band"],
    ),
    Measure(
        id="allmedrv12m_sex_rate",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["sex"],
    ),
    Measure(
        id="allmedrv12m_imdQ5_rate",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["imdQ5"],
    ),
    Measure(
        id="allmedrv12m_region_rate",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["region"],
    ),
    Measure(
        id="allmedrv12m_ethnicity_rate",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["ethnicity"],
    ),
    Measure(
        id="allmedrv12m_ethnicity16_rate",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["ethnicity16"],
    ),
    Measure(
        id="allmedrv12m_learning_disability_rate",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["learning_disability"],
    ),
    Measure(
        id="allmedrv12m_nhome_rate",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["nhome"],
    ),
    Measure(
        id="allmedrv12m_care_home_type_rate",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["care_home_type"],
    ),
    Measure(
        id="allmedrv12m_teratogenic_meds_rate",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["teratogenicmeds_last12m"],
    ),
    Measure(
        id="allmedrv12m_dmards_rate",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["dmards_last12m"],
    ),
    Measure(
        id="allmedrv12m_addictive_meds_rate",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["addictivemeds_last12m"],
    ),
    Measure(
        id="allmedrv12m_highrisk_meds_rate",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["highriskmeds_last12m"],
    ),
    ## Age Standardisation Measures
    Measure(
        id="allmedrv_population_rate_agesexstandardgrouped",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["AgeGroup", "sex"],
    ),
    Measure(
        id="allmedrv12m_population_rate_agesexstandardgrouped",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["AgeGroup", "sex"],
    ),
    Measure(
        id="allmedrv_practice_rate_agesexstandardgrouped",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["AgeGroup", "sex", "practice"],
    ),
    Measure(
        id="allmedrv_age_band_rate_agesexstandardgrouped",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["sex", "age_band"],
    ),
    Measure(
        id="allmedrv_sex_rate_agesexstandardgrouped",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["AgeGroup", "sex"],
    ),
    Measure(
        id="allmedrv_imdQ5_rate_agesexstandardgrouped",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["AgeGroup", "sex", "imdQ5"],
    ),
    Measure(
        id="allmedrv_region_rate_agesexstandardgrouped",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["AgeGroup", "sex", "region"],
    ),
    Measure(
        id="allmedrv_ethnicity_rate_agesexstandardgrouped",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["AgeGroup", "sex", "ethnicity"],
    ),
    Measure(
        id="allmedrv_ethnicity16_rate_agesexstandardgrouped",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["AgeGroup", "sex", "ethnicity16"],
    ),
    Measure(
        id="allmedrv_learning_disability_rate_agesexstandardgrouped",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["AgeGroup", "sex", "learning_disability"],
    ),
    Measure(
        id="allmedrv_nhome_rate_agesexstandardgrouped",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["AgeGroup", "sex", "nhome"],
    ),
    Measure(
        id="allmedrv_care_home_type_rate_agesexstandardgrouped",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["AgeGroup", "sex", "care_home_type"],
    ),
    Measure(
        id="allmedrv_teratogenic_meds_rate_agesexstandardgrouped",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["AgeGroup", "sex", "teratogenicmeds_last12m"],
    ),
    Measure(
        id="allmedrv_dmards_rate_agesexstandardgrouped",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["AgeGroup", "sex", "dmards_last12m"],
    ),
    Measure(
        id="allmedrv_addictive_meds_rate_agesexstandardgrouped",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["AgeGroup", "sex", "addictivemeds_last12m"],
    ),
    Measure(
        id="allmedrv_highrisk_meds_rate_agesexstandardgrouped",
        numerator="had_anymedrev",
        denominator="population",
        group_by=["AgeGroup", "sex","highriskmeds_last12m"],
    ),
    Measure(
        id="allmedrv12m_practice_rate_agesexstandardgrouped",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["AgeGroup", "sex", "practice"],
    ),
    Measure(
        id="allmedrv12m_age_band_rate_agesexstandardgrouped",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["sex", "age_band"],
    ),
    Measure(
        id="allmedrv12m_sex_rate_agesexstandardgrouped",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["AgeGroup", "sex"],
    ),
    Measure(
        id="allmedrv12m_imdQ5_rate_agesexstandardgrouped",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["AgeGroup", "sex", "imdQ5"],
    ),
    Measure(
        id="allmedrv12m_region_rate_agesexstandardgrouped",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["AgeGroup", "sex", "region"],
    ),
    Measure(
        id="allmedrv12m_ethnicity_rate_agesexstandardgrouped",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["AgeGroup", "sex", "ethnicity"],
    ),
    Measure(
        id="allmedrv12m_ethnicity16_rate_agesexstandardgrouped",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["AgeGroup", "sex", "ethnicity16"],
    ),
    Measure(
        id="allmedrv12m_learning_disability_rate_agesexstandardgrouped",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["AgeGroup", "sex", "learning_disability"],
    ),
    Measure(
        id="allmedrv12m_nhome_rate_agesexstandardgrouped",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["AgeGroup", "sex", "nhome"],
    ),
    Measure(
        id="allmedrv12m_care_home_type_rate_agesexstandardgrouped",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["AgeGroup", "sex", "care_home_type"],
    ),
    Measure(
        id="allmedrv12m_teratogenic_meds_rate_agesexstandardgrouped",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["AgeGroup", "sex", "teratogenicmeds_last12m"],
    ),
    Measure(
        id="allmedrv12m_dmards_rate_agesexstandardgrouped",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["AgeGroup", "sex", "dmards_last12m"],
    ),
    Measure(
        id="allmedrv12m_addictive_meds_rate_agesexstandardgrouped",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["AgeGroup", "sex", "addictivemeds_last12m"],
    ),
    Measure(
        id="allmedrv12m_highrisk_meds_rate_agesexstandardgrouped",
        numerator="had_anymedrev12m",
        denominator="population",
        group_by=["AgeGroup", "sex", "highriskmeds_last12m"],
    ),
]
