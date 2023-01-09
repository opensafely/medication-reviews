import tempfile
import pandas as pd
import numpy as np
from pathlib import Path
from pandas import testing
from analysis.table_1 import match_paths, update_df, fill_missing_values, subset_outcome_of_interest, get_counts


def test_match_paths():
    # Create a temporary directory
    temp_dir = tempfile.TemporaryDirectory()
    temp_dir = Path(temp_dir.name)
    
    # within the temporary directory, create a directory called output/joined
    (temp_dir / "output/joined").mkdir(parents=True, exist_ok=True)

    # Create a list of test files in the temporary directory (unordered)
    test_files = [
        "output/joined/input_2020-01-01.csv.gz",
        "output/joined/input_2020-03-01.csv.gz",
        "output/joined/input_2020-02-01.csv.gz",
        "output/input_2020-05-01.csv.gz" # This file should not be matched
    ]

    # Create the test files in the temporary directory
    for file in test_files:
        
        with open(temp_dir / file, 'w') as f:
            f.write('')
            print(f"Created {file} in {temp_dir}.")


    # Set the expected output for each test - note that the order of the files is important
    expected_output = [
        temp_dir / "output/joined/input_2020-01-01.csv.gz", 
        temp_dir / "output/joined/input_2020-02-01.csv.gz", 
        temp_dir / "output/joined/input_2020-03-01.csv.gz"
        ]
    
    # the observed outputs are absolute paths, so we need to convert the expected output to absolute paths
    expected_output = [Path(x).resolve() for x in expected_output]

    observed_output = match_paths(str(temp_dir / "output/joined/input_20*.csv.gz"))
    
    assert observed_output == expected_output


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

def test_update_df():
    original_df = pd.DataFrame(
        {
            "patient_id": pd.Series([1, 2, 3, 4, 5]),
            "age_band": pd.Series(['0-9', '10-19', '20-29', '30-39', '40-49']),
        })
    
    new_df = pd.DataFrame(
        {
            "patient_id": pd.Series([1, 2, 3, 4, 5, 6]),
            "age_band": pd.Series(['10-19', '10-19', '20-29', '40-49', "missing", '40-49']),
        })

    obs = update_df(original_df, new_df, columns=["age_band"])
    exp = pd.DataFrame(
        {
            "patient_id": pd.Series([1, 2, 3, 4, 5, 6]),
            "age_band": pd.Series(['10-19', '10-19', '20-29', '40-49', '40-49', '40-49']),
        })

    testing.assert_frame_equal(obs, exp)



