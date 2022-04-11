# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 10:49:09 2022

@author: jvorsten
"""

# Python imports
from itertools import filterfalse
import inspect
import unittest
import os
from datetime import datetime

# Third party imports
import pandas as pd
import numpy as np

# Local imports
from trendreview.GraphAll import GraphAll
from trendreview.reporting import FDDReporting
from trendreview.FDDExceptions import FDDException

# Read file into pandas dataframe
# Relative to project root (not relative to __file__)
FILEPATH = '../data/DD03.csv'
FILEPATH2 = '../data/dd64.csv'
FILEPATH3 = '../data/ddvav_test.csv'
LOG_FILEPATH = '../reports/testreport.txt'

#%%

class TestGraphAll(unittest.TestCase):
    
    def setUp(self):
        
        self.data = pd.read_csv(FILEPATH, sep=',', parse_dates=['DateTime'])
        self.data3 = pd.read_csv(FILEPATH3, sep=',', parse_dates=['DateTime'])
        self.graphall = GraphAll(FILEPATH3)
        
        return None
    
    def test_graph_all_data(self):
        independent_axis_name = 'DateTime'
        dependent_axis_names = None # Graph all
        reporter = FDDReporting(log_filepath=LOG_FILEPATH)
        self.graphall.graph_all_data(reporter, independent_axis_name, dependent_axis_names)
        return None
    
    def test_(self):
        return None
    
    def test_(self):
        return None

if __name__ == '__main__':
    unittest.main()
    
    # Alternate methods
    # def suite():
    #     suite = unittest.TestSuite()
    #     suite.addTest(TestDDVAV('test_rule_simultaneous_heating_cooling'))
    #     suite.addTest(TestDDVAV('test_rule_room_temperature_deviation'))
    #     return suite
    # runner = unittest.TextTestRunner()
    # runner.run(suite())