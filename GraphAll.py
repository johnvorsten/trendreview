# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 14:27:06 2022

@author: jvorsten

Logic for fault detection and trend review including single duct terminal units
See documentation for list of rules covered

Logic
1. Load data
2. Graph each data point versus DateTime
"""

# Python imports
from typing import List, Callable
import inspect
import math

# Third party imports
import pandas as pd
import numpy as np

# Local imports
from FDDExceptions import FDDException
from reporting import FDDReporting
from helpers import (masked_consecutive_elements, 
                     _datetimes_to_seconds_deviation_from_start,
                     _hour_segment_indices_from_seconds,
                     )
# Declarations
HEADERS = ['DateTime',
                 ]
TYPES = {'DateTime':object,
                }

#%%


class GraphAll:
    """Collection of rules to check on trended data for dual-duct terminal
    units"""
    
    def __init__(self, filepath: str):
        """Inputs
        ------
        filepath: (string) name of CSV file related to a dual-duct terminal
        unit to open, parse, and apply rule checks to"""
        
        self.csv_filepath = filepath
        self.data = pd.read_csv(filepath, sep=',', parse_dates=['DateTime'])
        
        return None
    
    def evaluate_rules(self, methods: List[Callable[[pd.DataFrame],None]], 
                       reporter: FDDReporting) -> None:
        """This is a convenience function which calls each of the methods
        passed to it, and catches FDDExceptions thrown by each rule, then logs
        the exceptions
        
        Example
        sdvavRules = SDVAVRules(filepath)
        methods = sdvavRules.get_rules()
        reporter = FDDReporting(log_filepath=log_filepath)
        sdvavRules.evaluate_rules(methods, reporter)
        # Results of faults detected in `filepath`
        """
        for method in methods:
            try:
                method(self.data)
            except FDDException as e:
                reporter.log_exception(e, create_image=True)
        return None
    
    def get_rules(self):
        """Get all class member functions that start with 'rule_'"""
        
        methods = []
        for name in dir(self):
            attribute = getattr(self, name)
            if inspect.ismethod(attribute) and str(attribute).__contains__('.rule_'):
                methods.append(attribute)
        
        return methods