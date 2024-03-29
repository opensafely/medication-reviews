import pytest
import pandas as pd
import numpy as np
from pandas import testing
from analysis.correct_age_groups import regroupAgeGroup, regroupage_band
#from hypothesis import strategies as st
#from hypothesis import assume, given


@pytest.fixture()
def test_table():
    """Returns a test table produced by correct_age_groups.py."""
    return pd.DataFrame(
        {
            "AgeGroup": pd.Series(["15-19", "15-19", "15-19", "15-19", "15-19", "15-19", "15-19", "15-19", "20-24", "20-24", "20-24", "20-24", "20-24", "20-24", "20-24", "20-24", "40-44", "40-44", "40-44", "40-44", "40-44", "40-44", "40-44", "40-44"]),
            "sex": pd.Series(['F', 'F', 'M', 'M', 'F', 'F', 'M', 'M', 'F', 'F', 'M', 'M', 'F', 'F', 'M', 'M', 'F', 'F', 'M', 'M', 'F', 'F', 'M', 'M']),
            "demographic": pd.Series([0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]),
            "numerator": pd.Series([10, 20, 30, 40, 50, 60, 70, 80, 15, 25, 35, 45, 55, 65, 75, 85, 1, 2, 3, 4, 5, 6, 7, 8]),
            "population": pd.Series([102, 135, 156, 120, 158, 177, 192, 188, 144, 123, 168, 124, 157, 123, 147, 195, 145, 167, 147, 178, 136, 137, 157, 147]),
            "date": pd.Series(["01/04/2019", "01/04/2019", "01/04/2019", "01/04/2019", "01/05/2019", "01/05/2019", "01/05/2019", "01/05/2019", "01/04/2019", "01/04/2019", "01/04/2019", "01/04/2019", "01/05/2019", "01/05/2019", "01/05/2019", "01/05/2019", "01/04/2019", "01/04/2019", "01/04/2019", "01/04/2019", "01/05/2019", "01/05/2019", "01/05/2019", "01/05/2019"]),
        }
    )

@pytest.fixture()
def test_table_age_bands():
    """Returns a test table produced by correct_age_groups.py."""
    return pd.DataFrame(
        {
            "AgeGroup": pd.Series(["18-24", "18-24", "40-44", "18-24", "18-24"]),
            "sex": pd.Series(['F', 'F', 'M', 'F', 'F']),
            "age_band": pd.Series(["0-19", "20-29", "40-49", "0-19", "20-29"]),
            "numerator": pd.Series([10, 10, 50, 75, 25]),
            "population": pd.Series([20, 20, 200, 75, 25]),
            "date": pd.Series(["01/04/2019", "01/04/2019", "01/04/2019", "01/05/2019", "01/05/2019"]),
        }
    )

def test_regroupAgeGroup(test_table):
    obs = regroupAgeGroup(test_table, "demographic", "numerator")
    
    exp = pd.DataFrame(
        {
            "AgeGroup": pd.Series(["18-24", "18-24", "18-24", "18-24", "40-44", "40-44", "40-44", "40-44", "18-24", "18-24", "18-24", "18-24", "40-44", "40-44", "40-44", "40-44"]),
			"sex": pd.Series(['F', 'F', 'M', 'M', 'F', 'F', 'M', 'M', 'F', 'F', 'M', 'M', 'F', 'F', 'M', 'M']),
			"demographic": pd.Series([0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]),
			"date": pd.Series(["01/04/2019", "01/04/2019", "01/04/2019", "01/04/2019",  "01/04/2019", "01/04/2019", "01/04/2019", "01/04/2019", "01/05/2019", "01/05/2019", "01/05/2019", "01/05/2019", "01/05/2019", "01/05/2019", "01/05/2019", "01/05/2019"]),       
            "numerator": pd.Series([25, 45, 65, 85, 1, 2, 3, 4, 105, 125, 145, 165, 5, 6, 7, 8]),
            "population": pd.Series([246, 258, 324, 244, 145, 167, 147, 178,  315, 300, 339, 383, 136, 137, 157, 147]),
            "value": pd.Series([0.1016260162601626, 0.1744186046511628, 0.2006172839506173, 0.3483606557377049, 0.0068965517241379, 0.0119760479041916, 0.0204081632653061, 0.0224719101123596, 0.3333333333333333, 0.4166666666666667, 0.4277286135693215, 0.4308093994778068, 0.0367647058823529, 0.0437956204379562, 0.0445859872611465, 0.054421768707483])
        }
    )
    testing.assert_frame_equal(obs.reset_index(drop=True), exp.reset_index(drop=True), check_dtype=True)

def test_regroupageband(test_table_age_bands):
    obs = regroupage_band(test_table_age_bands, "numerator")
    
    exp = pd.DataFrame(
        {
            "sex": pd.Series(['F', 'M', 'F']),
            "age_band": pd.Series(["18-29", "40-49", "18-29"]),
            "date": pd.Series(["01/04/2019", "01/04/2019", "01/05/2019"]),
            "numerator": pd.Series([20, 50, 100]),
            "population": pd.Series([40, 200, 100]),
            "value": pd.Series([0.5, 0.25, 1])
        }
    )
    testing.assert_frame_equal(obs.reset_index(drop=True), exp.reset_index(drop=True), check_dtype=True)