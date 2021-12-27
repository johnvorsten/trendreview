# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 14:15:57 2021

Custom exceptions raised during fault detection

@author: jvorsten
"""

# Python imports
from typing import List, MutableMapping

# Third party imports
import pandas as pd

# Local imports

#%%

class FDDException(Exception):
    """Base class for exceptions on fault detection and diagnostics"""
    
    def __init__(self, message: str, data: MutableMapping[str, List]):
        self.message = message
        self.data = data
        return None

