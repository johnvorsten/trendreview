# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 11:02:54 2021

@author: jvorsten
"""

# Python imports
import unittest

# Thrid party imports
import numpy as np
import pandas as pd

# Local imports
from trendreview.helpers import read_csv, _correct_time_str_HM, _parse_date_time_str_YmdHM
from trendreview.ddvav import DDVAV_HEADERS, DDVAV_TYPES

# Read file into pandas dataframe
FILEPATH = '../data/DD03.csv'
FILEPATH2 = '../data/dd64.csv'

# %%

class TestNumpyDateTimeIterables(unittest.TestCase):
    """Convert datetime strings to numpy iterables"""

    def test_date_time_iterables_to_numpy(self):

        data = read_csv(FILEPATH, DDVAV_HEADERS, DDVAV_TYPES)

        dates = [str(x.date()) for x in data["Date"]]
        times = _correct_time_str_HM(data["Time"].to_list())

        datetimes = _parse_date_time_str_YmdHM(dates, times)

        return None


if __name__ == '__main__':
    unittest.main()
