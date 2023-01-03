import pytest
import pandas as pd
import numpy as np
from pandas import testing
import correct_age_groups
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

def test_regroupAgeGroup(test_table):
    obs = correct_age_groups.regroupAgeGroup(test_table, "demographic", "numerator")
    
    exp = pd.DataFrame(
        {
            "AgeGroup": pd.Series(["18-24", "18-24", "18-24", "18-24", "40-44", "40-44", "40-44", "40-44", "18-24", "18-24", "18-24", "18-24", "40-44", "40-44", "40-44", "40-44"]),
			"sex": pd.Series(['F', 'F', 'M', 'M', 'F', 'F', 'M', 'M', 'F', 'F', 'M', 'M', 'F', 'F', 'M', 'M']),
			"demographic": pd.Series([0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]),
			"date": pd.Series(["01/04/2019", "01/04/2019", "01/04/2019", "01/04/2019",  "01/04/2019", "01/04/2019", "01/04/2019", "01/04/2019", "01/05/2019", "01/05/2019", "01/05/2019", "01/05/2019", "01/05/2019", "01/05/2019", "01/05/2019", "01/05/2019"]),           
            "numerator": pd.Series([25, 45, 65, 85, 1, 2, 3, 4, 105, 125, 145, 165, 5, 6, 7, 8]),
            "population": pd.Series([246, 258, 324, 244, 145, 167, 147, 178,  315, 300, 339, 383, 136, 137, 157, 147]),
        }
    )

    testing.assert_frame_equal(obs.reset_index(drop=True), exp.reset_index(drop=True), check_dtype=True)