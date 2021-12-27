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
from helpers import read_csv, masked_consecutive_elements

#%%

# Read file into pandas dataframe
filepath = './data/DD03.csv'
filepath2 = './data/dd64.csv'

data = read_csv(filepath, DDVAV_HEADERS, DDVAV_TYPES)

class TestDDVAV(unittest.TestCase):
    
    def setUp(self):
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
