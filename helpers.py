# -*- coding: utf-8 -*-
"""
Created on Mon Dec 27 15:39:47 2021

@author: jvorsten
"""

# Python imports
from Typing import List

# Thrid party imports
import numpy as np
import pandas as pd

# Local imports

#%%

def read_csv(filepath, headers, dtypes):
    """Wrapper for pandas read_csv method. Read a CSV file into a dataframe
    object with the specified types for dual-duct VAV units.
    This method enforces datatypes and headers for the input CSV file
    format"""
    df = pd.read_csv(filepath, sep=',', usecols=headers,
                     parse_dates=['Date'], dtype=dtypes)
    return df

def masked_consecutive_elements(data: np.ma.MaskedArray, n_consecutive_elements: int) -> List[int]:
    """Return indices where a masked array is True for n_consecutive_elements
    for rising edge only
    inputs
    -------
    data: (np.ma.MaskedArray) array of 0,1 representing a test condition. This
    function reports consecutive 1s
    output
    -------
    rising_edge: list[int] of indices where there are consecutive elements
    example
    data = np.ma.MaskedArray([0,0,0,0,1,1,1,0,0,0,1,1,1])
    res = masked_consecutive_elements(data, 3) # [4, 10]
    >>> res
    out: [4, 10]
    """
    rising_edge = []
    pushed = False
    consecutive_count = 0
    
    for i in range(0, data.shape[0]):
        if data[i]:
            consecutive_count += 1
            if consecutive_count == n_consecutive_elements and not pushed:
                rising_edge.append(i - n_consecutive_elements + 1)
                pushed = True
        else:
            consecutive_count = 0
            pushed = False
        
    return rising_edge

def masked_rolling_sum(data: np.ma.MaskedArray, n_consecutive_elements: int):
    """Return the indices of a masked array that contain 'n' consecutive 
    True elements"""
    window_sum = np.zeros((data.shape[0] - n_consecutive_elements))
    for i in range(0, data.shape[0] - n_consecutive_elements):
        window_sum[i] = np.sum(data[i:n_consecutive_elements])
    
    return np.where(window_sum == n_consecutive_elements)