import pytest
import pandas as pd
import numpy as np
from pandas import testing
from analysis.rate_calculations_demographics import standardise_rates_agesex_apply
#from hypothesis import strategies as st
#from hypothesis import assume, given


@pytest.fixture()
def test_table():
    """Returns a test table"""
    return pd.DataFrame(
        {
            "AgeGroup": pd.Series(["18-24"]),
            "sex": pd.Series(["F"]),
            "demographic": pd.Series([0]),
            "date": pd.Series(["01/04/2019"]),
            "numerator": pd.Series([10]),
            "population": pd.Series([20]),
            "age_rates": pd.Series([0.0002]),
        }
    )

@pytest.fixture()
def test_agesex_stand_pop():
    """Returns a test standard pop table"""
    return pd.DataFrame(
        {
            "age_stand": pd.Series(["18-24"]),
            "sex": pd.Series(["F"]),
            "uk_pop_ratio": pd.Series([0.05]),
        }
    )

#def test_agesex_standardise(test_table, test_agesex_stand_pop):
    #obs = standardise_rates_agesex_apply(test_table, test_agesex_stand_pop)
    #INCOMPLETE

