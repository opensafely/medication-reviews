import pytest
import pandas as pd
import numpy as np
from pandas import testing
import redaction_utils
#from hypothesis import strategies as st
#from hypothesis import assume, given


@pytest.fixture()
def codeuse_table():
    """Returns a codeuse table produced by code_use_summary.py."""
    return pd.DataFrame(
        {
            "code": pd.Series([1, 2, 3, 4, 5]),
            "term": pd.Series(['term1', 'term2', 'term3', 'term4', 'term5']),
            "termcode": pd.Series(['term1 (1)', 'term2 (2)', 'term3 (3)', 'term4 (4)', 'term5 (5)']),
            "uses": pd.Series([0, 0, 0, 0, 41]),
        }
    )

def test_redact_events_table(codeuse_table):
    obs = redaction_utils.codeuse_redact_small_numbers(codeuse_table, n=7, rounding_base=5, column="uses")
    
    exp = pd.DataFrame(
            {
                "code": pd.Series([1, 2, 3, 4, 5]),
                "term": pd.Series(['term1', 'term2', 'term3', 'term4', 'term5']),
                "termcode": pd.Series(['term1 (1)', 'term2 (2)', 'term3 (3)', 'term4 (4)', 'term5 (5)']),
                "uses": pd.Series([0, 0, 0, 0, 40]),
            }
        )
    testing.assert_frame_equal(obs, exp, check_dtype=False)
