# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 16:29:57 2021

@author: jvorsten
"""

# Python imports
from itertools import filterfalse
import inspect
import unittest

# Third party imports
import pandas as pd
import numpy as np

# Local imports
from ddvav import (DDVAVRules, DDVAV_TYPES, DDVAV_HEADERS)
from helpers import (read_csv, masked_consecutive_elements, 
                     _datetimes_to_seconds_deviation_from_start)

# Read file into pandas dataframe
FILEPATH = './data/DD03.csv'
FILEPATH2 = './data/dd64.csv'

#%%




class TestDDVAV(unittest.TestCase):
    
    def setUp(self):
        data = data = read_csv(FILEPATH, DDVAV_HEADERS, DDVAV_TYPES)
        return None
    
    def test_masked_consecutive_elements(self):
        # Rising edge at indicy 3
        data = np.ma.MaskedArray([0,0,0,1,1,1,1,0,0,0])
        res = masked_consecutive_elements(data, 3)
        self.assertEqual(res, [3])
        
        data = np.ma.MaskedArray([0,0,1,1,1,1,1,0,0,0])
        res = masked_consecutive_elements(data, 3)
        self.assertEqual(res, [2])
        
        data = np.ma.MaskedArray([1,1,1,1,1,1,1,0,0,0])
        res = masked_consecutive_elements(data, 3)
        self.assertEqual(res, [0])
        
        data = np.ma.MaskedArray([0,0,0,0,1,1,1,0,0,0])
        res = masked_consecutive_elements(data, 3)
        self.assertEqual( res, [4])
        
        data = np.ma.MaskedArray([0,0,0,0,1,1,1,0,0,0,1,1,1])
        res = masked_consecutive_elements(data, 3)
        self.assertEqual(res, [4,10])
        
        return None
    
    def test_integration_over_time(self):
        
        # Theory testing
        control = [10] * 5 # setpoint
        process = [7,8,9,10,11] # process variable
        
        diff = np.array(control) - np.array(process)
        
        # Prepare datetime to integrate over
        datetimes = np.array(['2021-12-18T10:00:00', 
                              '2021-12-18T10:05:00', # 5 minute interval
                              '2021-12-18T10:10:00',
                              '2021-12-18T10:20:00', # 10 minute interval
                              '2021-12-18T10:35:00', # 15 minute interval
                              ], dtype='datetime64[s]')
        xs = _datetimes_to_seconds_deviation_from_start(datetimes)
        
        # Integrations
        deviation = np.trapz(y=diff) # 4.0, with 1 unit x inferred
        # with defined time interval
        deviation_time = np.trapz(y=diff, x=datetimes) # 1050 / 60 = 17.5
        # Defined time interval in minutes
        deviation_equ = np.trapz(y=diff, x=[0,5,10,20,35]) # 17.5
        
        return None