# -*- coding: utf-8 -*-
"""
Created on 2022-4-13

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
from trendreview.trendreview import parser

# Read file into pandas dataframe
# Relative to project root (not relative to __file__)
FILEPATH = '../data/ddvav_test.csv'

#%%

class TestGraphAll(unittest.TestCase):
    
    def test_parse_args_inclusive(self):
        
        args = ['--filepath', FILEPATH, '--type', 'ddvav', '--report-path', './custom-report.txt',
                '--graph-columns', 'column a','column b', 'column c', '--datetime-header', 'timestamp']
        namespace = parser.parse_args(args)
        filepath = os.path.abspath(namespace.filepath)
        equipment_type = namespace.type
        log_filepath = os.path.abspath(namespace.log_filepath.name)
        namespace.log_filepath.close()
        independent_axis_name = namespace.independent_axis_name
        graph_columns = namespace.graph_columns
        self.assertEqual(independent_axis_name, 'timestamp')
        self.assertListEqual(graph_columns, ['column a','column b', 'column c'])
        print(namespace)

        return None

    def test_parse_args_graph_columns_default(self):

        args = ['--filepath', FILEPATH, '--type', 'ddvav', '--report-path', './custom-report.txt',
                '--datetime-header', 'timestamp']
        namespace = parser.parse_args(args)
        graph_columns = namespace.graph_columns
        self.assertEqual(graph_columns, None)
        print('Namespace without --graph-columns : ', namespace)

        return None

    def test_parse_args_datetime_header_default(self):

        args = ['--filepath', FILEPATH, '--type', 'ddvav', '--report-path', './custom-report.txt']
        namespace = parser.parse_args(args)
        independent_axis_name = namespace.independent_axis_name
        self.assertEqual(independent_axis_name, 'DateTime')
        print('Namespace without --graph-columns : ', namespace)

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