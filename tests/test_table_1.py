import pandas as pd
import numpy as np
from pandas import testing
from analysis.table_1 import update_df, fill_missing_values, subset_outcome_of_interest, get_counts

def test_fill_missing_values():
    df = pd.DataFrame(
        {
            "patient_id": pd.Series([1, 2, 3, 4, 5]),
            "demographic": pd.Series(['M', 'F', np.nan, 'M', np.nan]),
         
        }
    )
    obs = fill_missing_values(df, ["demographic"])
    exp = pd.DataFrame(
        {
            "patient_id": pd.Series([1, 2, 3, 4, 5]),
            "demographic": pd.Series(['M', 'F', 'missing', 'M', 'missing']),
         
        }
    )
   
    testing.assert_frame_equal(obs, exp)

def test_subset_outcome_of_interest():
    df = pd.DataFrame(
        {
            "patient_id": pd.Series([1, 2, 3, 4, 5]),
            "demographic": pd.Series(['M', 'F', 'M', 'M', 'F']),
            "outcome": pd.Series([1, 0, 0, 1, 1]),
         
        }
    )
    obs, obs_outcome = subset_outcome_of_interest(df, "outcome")

    exp = pd.DataFrame(
        {
            "patient_id": pd.Series([1, 2, 3, 4, 5]),
            "demographic": pd.Series(['M', 'F', 'M', 'M', 'F'])
         
        }
    )

    exp_outcome = pd.DataFrame(
        {
            "patient_id": pd.Series([1, 4, 5]),
            "demographic": pd.Series(['M', 'M', 'F'])
         
        }
    )

    testing.assert_frame_equal(obs_outcome, exp_outcome)
    testing.assert_frame_equal(obs, exp)

def test_get_counts():
    df = pd.DataFrame(
        {
            "patient_id": pd.Series([1, 2, 3, 4, 5]),
            "sex": pd.Series(['M', 'F', 'M', 'M', 'F']),
            "age_band": pd.Series(['0-9', '10-19', '20-29', '30-39', '40-49']),
         
        }
    )
    obs = get_counts(df)
    
    exp = pd.Series([2, 3, 1, 1, 1, 1, 1], dtype="float64")
    exp.index = pd.MultiIndex.from_tuples(
        [("sex", "F"), ("sex", "M"), ("age_band", "0-9"), ("age_band", "10-19"), ("age_band", "20-29"), ("age_band", "30-39"), ("age_band", "40-49")],
    )
    exp.name = "count"

    testing.assert_series_equal(obs, exp)



