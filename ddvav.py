# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 16:11:17 2021

@author: jvorsten

Logic for fault detection and trend review including dual duct terminal units
See documentation for list of rules covered

Logic
1. Load data into pandas dataframe
2. Apply rules along data (see rules)
3. If a rule check is broken, then raise a custom exception (or possibly only 
send a message to a reporting class.. not sure about raising an exception)
4. The exception will be caught the the calling function and handed to the 
reporting class which logs the broken rule
5. The exception will be handed to a plotting class which will create a plot
of the broken rule, and apply visual formatting. The plot is saved to a 
configurable location
6. 
"""

# Python imports
from typing import List
from itertools import filterfalse
import inspect
import math

# Third party imports
import pandas as pd
import numpy as np

# Local imports
from FDDExceptions import FDDException
from helpers import masked_consecutive_elements

# Declarations
DDVAV_HEADERS = ['Date', 'Time', 'DischargeTemperature', 'CoolingDamperCommand',
                 'CooingDamperPosition', 'CoolingAirVolume', 'CoolingSetpoint',
                 'ControlTemperature', 'ScheduleMode', 'OccupancyMode',
                 'HeatCoolMode', 'HeatingDamperCommand', 'HeatingDamperPosition',
                 'HeatingAirVolume', 'RoomTemperature', 'AirflowSetpoint']
DDVAV_TYPES = {'Date':object, 
               'Time':str, 
               'DischargeTemperature':np.float32, 
               'CoolingDamperCommand':np.float32,
               'CooingDamperPosition':np.float32, 
               'CoolingAirVolume':np.float32, 
               'CoolingSetpoint':np.float32,
               'ControlTemperature':np.float32, 
               'ScheduleMode':np.int8, 
               'OccupancyMode':bool,
               'HeatCoolMode':str, 
               'HeatingDamperCommand':np.float32, 
               'HeatingDamperPosition':np.float32,
               'HeatingAirVolume':np.float32, 
               'RoomTemperature':np.float32, 
               'AirflowSetpoint':np.float32,
                }

#%%

def maximum_allowed_failures(mask: np.ma.MaskedArray,
                             data: pd.DataFrame,
                             failure_percent: float, 
                             report_columns: List[str],
                             error_msg:str) -> None:
    """Raise a FDDException if the maximum number of failures within a mask is 
    exceeded"""
    
    max_failures = math.floor(failure_percent * len(mask))
    if mask.sum() > max_failures:
        report_indices = mask.nonzero()[0][:max_failures]
        data_view = data.loc[report_indices, report_columns].to_dict(orient='list')
        gmsg=("The maximum allowed instances ({} at {:.0%} of samples) was "+
             "exceeded ({} observed)")
        msg = error_msg + "\n" + gmsg
        msg=msg.format(max_failures, failure_percent, mask.sum())
        raise FDDException(msg, data_view)
            
    return None

def maximum_consecutive_failures(mask: np.ma.MaskedArray,
                                 data: pd.DataFrame,
                                 failure_consecutive: float, 
                                 report_columns: List[str],
                                 error_msg:str) -> None:
    
    consecutive_indices = masked_consecutive_elements(mask, failure_consecutive)
    if len(consecutive_indices) > 0:
        report_indices = consecutive_indices
        data_view = data.loc[report_indices, report_columns].to_dict(orient='list')
        gmsg=("The maximum allowed consecutive instances ({}) was exceeded "+
              "({} observed)")
        msg = error_msg + "\n" + gmsg
        msg=msg.format(failure_consecutive, len(consecutive_indices))
        raise FDDException(msg, data_view)
            
    return None

class DDVAVRules:
    """Collection of rules to check on trended data for dual-duct terminal
    units"""
    
    def __init__(self):
        """Inputs
        ------
        filepath: (string) name of CSV file related to a dual-duct terminal
        unit to open, parse, and apply rule checks to"""
        
        return None
    
    def __call__(self):
        # Get all methods that start with 'rule_'
        methods = self._get_rules()
        # Iterate through each 'rule_' method and call it
        for method in methods:
            method()
        return None
    
    def _get_rules(self):
        """Get all class member functions that start with 'rule_'"""
        
        methods = []
        for name in dir(self):
            attribute = getattr(self, name)
            if inspect.ismethod(attribute) and str(attribute).__contains__('.rule_'):
                methods.append(attribute)
        
        return methods
    
    @classmethod
    def rule_simultaneous_heating_cooling(cls, data: pd.DataFrame):
        """Iterate over heating and cooling airflow values. 
        Rule fails if - 
        1. heating and cooling volumetric flow is overlapping, where airflow > 
        0 for either heating or cooling duct while the other duct is > 0 for 
        more than n% ofobservations OR n consecutive observations"""
        # Tolerance for considering airflow at zero
        tolerance = 10
        failure_percent = 0.02
        failure_consecutive = 3
        
        # masking and comparisons
        heating = np.ma.array(data["HeatingAirVolume"] > tolerance)
        cooling = np.ma.array(data["CoolingAirVolume"] > tolerance)
        overlap = np.bitwise_and(heating, cooling) # masked array
        overlap_indices = overlap.nonzero()
        
        # Failure condition n% ofovservations
        max_overlap = math.floor(failure_percent * len(heating))
        if overlap.sum() > max_overlap:
            report_indices = overlap_indices[0][:max_overlap]
            data_view = data.loc[report_indices, ["Date","Time","HeatingAirVolume","CoolingAirVolume"]].to_dict(orient='list')
            msg=("The maximum allowed instances of simultaneous heating and "+
                 "cooling ({} at {:.0%} of samples) was exceeded ({} observed)")
            msg=msg.format(max_overlap, failure_percent, overlap.sum())
            raise FDDException(msg, data_view)
        
        # Failure condition n consecutive observations
        consecutive_indices = masked_consecutive_elements(overlap, failure_consecutive)
        if len(consecutive_indices) > 0:
            report_indices = consecutive_indices
            data_view = data.loc[report_indices, ["Date","Time","HeatingAirVolume","CoolingAirVolume"]].to_dict(orient='list')
            msg=("The maximum allowed consecutive instances of heating and "+
                 "cooling ({}) was exceeded ({} observed)")
            msg=msg.format(failure_consecutive, len(consecutive_indices))
            raise FDDException(msg, data_view)
            
        return None
    
    @classmethod
    def rule_heating_opposed_mode(cls, data: pd.DataFrame):
        """Iterate over heating and cooling airflow values. 
        Rule fails if - 
        1. heating/cooling occurs with the incorrect state in HeatCoolMode
        HeatingAirVolume > 0 when HeatCoolMode is in 'COOL'
        CoolingAirVolume > 0 when HeatCoolMode is in 'HEAT'
        """
        # Tolerance for considering airflow at zero
        tolerance = 10
        failure_percent = 0.02
        failure_consecutive = 3
        report_columns = ["Date","Time","HeatingAirVolume","HeatCoolMode"]
        
        # masking and comparisons
        heating = np.ma.array(data["HeatingAirVolume"] > tolerance)
        cooling_mode = np.ma.array(data["HeatCoolMode"] == "COOL")
        overlap = np.bitwise_and(heating, cooling_mode) # masked array
        overlap_indices = overlap.nonzero()
        
        # Failure condition n% ofovservations
        max_overlap = math.floor(failure_percent * len(heating))
        if overlap.sum() > max_overlap:
            report_indices = overlap_indices[0][:max_overlap]
            data_view = data.loc[report_indices, report_columns].to_dict(orient='list')
            msg=("The maximum allowed instances of heating in cooling mode "+
                 "({} at {:.0%} of samples) was exceeded ({} observed)")
            msg=msg.format(max_overlap, failure_percent, overlap.sum())
            raise FDDException(msg, data_view)
        
        # Failure condition n consecutive observations
        consecutive_indices = masked_consecutive_elements(overlap, failure_consecutive)
        if len(consecutive_indices) > 0:
            report_indices = consecutive_indices
            data_view = data.loc[report_indices, report_columns].to_dict(orient='list')
            msg=("The maximum allowed consecutive instances of heating and "+
                 "cooling ({}) was exceeded ({} observed)")
            msg=msg.format(failure_consecutive, len(consecutive_indices))
            raise FDDException(msg, data_view)
            
        return None
    
    @classmethod
    def rule_cooling_opposed_mode(cls, data: pd.DataFrame):
        """Iterate over heating and cooling airflow values. 
        Rule fails if - 
        1. heating/cooling occurs with the incorrect state in HeatCoolMode
        HeatingAirVolume > 0 when HeatCoolMode is in 'COOL'
        CoolingAirVolume > 0 when HeatCoolMode is in 'HEAT'
        """
        # Tolerance for considering airflow at zero
        tolerance = 10
        failure_percent = 0.02
        failure_consecutive = 3
        report_columns = ["Date","Time","CoolingAirVolume","HeatCoolMode"]
        
        # masking and comparisons
        cooling = np.ma.array(data["CoolingAirVolume"] > tolerance)
        heating_mode = np.ma.array(data["HeatCoolMode"] == "HEAT")
        overlap = np.bitwise_and(cooling, heating_mode) # masked array
        overlap_indices = overlap.nonzero()
        
        # Failure condition n% ofovservations
        max_overlap = math.floor(failure_percent * len(cooling))
        if overlap.sum() > max_overlap:
            report_indices = overlap_indices[0][:max_overlap]
            data_view = data.loc[report_indices, report_columns].to_dict(orient='list')
            msg=("The maximum allowed instances of heating in cooling mode "+
                 "({} at {:.0%} of samples) was exceeded ({} observed)")
            msg=msg.format(max_overlap, failure_percent, overlap.sum())
            raise FDDException(msg, data_view)
        
        # Failure condition n consecutive observations
        consecutive_indices = masked_consecutive_elements(overlap, failure_consecutive)
        if len(consecutive_indices) > 0:
            report_indices = consecutive_indices
            data_view = data.loc[report_indices, report_columns].to_dict(orient='list')
            msg=("The maximum allowed consecutive instances of heating and "+
                 "cooling ({}) was exceeded ({} observed)")
            msg=msg.format(failure_consecutive, len(consecutive_indices))
            raise FDDException(msg, data_view)
            
        return None
    
    @classmethod
    def rule_cooling_damper_stuck(cls, data: pd.DataFrame):
        """Damper position does not match damper command
        Rule fails if - 
        1. Damper position and command are >5% different
        """
        # configuration
        tolerance = 5
        failure_percent = 0.02
        failure_consecutive = 3
        report_columns = ["Date","Time","CoolingDamperCommand",
                          "CoolingDamperPosition"]
        error_msg=("Cooling damper stuck open: damper command and position "+
                   "are >5% different")
        
        # masking and comparisons
        diff = np.abs(np.array(data["CoolingDamperCommand"] - data["CoolingDamperPosition"]))
        mask = np.ma.array(diff > tolerance)
        
        # Failure condition n% of ovservations
        maximum_allowed_failures(mask, data, failure_percent, report_columns, error_msg)
        
        # Failure condition n consecutive observations
        maximum_consecutive_failures(mask, data, failure_consecutive, report_columns, error_msg)
        
        return None
        
    @classmethod
    def rule_heating_damper_stuck(cls, data: pd.DataFrame):
        """Damper position does not match damper command
        Rule fails if - 
        1. Damper position and command are >5% different
        """
        # configuration
        tolerance = 5
        failure_percent = 0.02
        failure_consecutive = 3
        report_columns = ["Date","Time","HeatingDamperCommand",
                          "HeatingDamperPosition"]
        error_msg=("Heating damper stuck open: damper command and position "+
                   "are >5% different")
        
        # masking and comparisons
        diff = np.abs(np.array(data["HeatingDamperCommand"] - data["HeatingDamperPosition"]))
        mask = np.ma.array(diff > tolerance)
        
        # Failure condition n% of ovservations
        maximum_allowed_failures(mask, data, failure_percent, report_columns, error_msg)
        
        # Failure condition n consecutive observations
        maximum_consecutive_failures(mask, data, failure_consecutive, report_columns, error_msg)
        
        return None
        
    @classmethod
    def rule_cooling_airflow_on_closed_damper(cls, data: pd.DataFrame):
        """Airflow is calculated to pass by damper when damper is commanded
        closed
        Rule fails if - 
        1. Airflow is greater than 10[cfm](default) AND damper position is 
        <2[%](default)"""
        # Tolerance for considering airflow at zero
        tolerance = 10
        tolerance_damper = 2 # percent
        failure_percent = 0.02
        failure_consecutive = 3
        report_columns = ["Date","Time","CoolingAirVolume","CoolingDamperPosition"]
        error_msg=("Airflow measured while damper is closed:")
        
        # masking and comparisons
        airflow = np.ma.array(data["CoolingAirVolume"] > tolerance)
        damper_closed = np.ma.array(data["CoolingDamperPosition"] < tolerance_damper)
        mask = np.bitwise_and(airflow, damper_closed) # masked array
        
        # Failure condition n% of ovservations
        maximum_allowed_failures(mask, data, failure_percent, report_columns, error_msg)
        
        # Failure condition n consecutive observations
        maximum_consecutive_failures(mask, data, failure_consecutive, report_columns, error_msg)
        
        return None
    
    @classmethod
    def rule_heating_airflow_on_closed_damper(cls, data: pd.DataFrame):
        """Airflow is calculated to pass by damper when damper is commanded
        closed
        Rule fails if - 
        1. Airflow is greater than 10[cfm](default) AND damper position is 
        <2[%](default)"""
        # Tolerance for considering airflow at zero
        tolerance = 10
        tolerance_damper = 2 # percent
        failure_percent = 0.02
        failure_consecutive = 3
        report_columns = ["Date","Time","HeatingAirVolume","HeatingDamperPosition"]
        error_msg=("Airflow measured while damper is closed:")
        
        # masking and comparisons
        airflow = np.ma.array(data["HeatingAirVolume"] > tolerance)
        damper_closed = np.ma.array(data["HeatingDamperPosition"] < tolerance_damper)
        mask = np.bitwise_and(airflow, damper_closed) # masked array
        
        # Failure condition n% of ovservations
        maximum_allowed_failures(mask, data, failure_percent, report_columns, error_msg)
        
        # Failure condition n consecutive observations
        maximum_consecutive_failures(mask, data, failure_consecutive, report_columns, error_msg)
        
        return None
        
    @classmethod
    def rule_damper_position_airflow_relationship(cls, data: pd.DataFrame):
        return None
            
    @classmethod
    def rule_room_temperature_deviation(cls, data: pd.DataFrame):
        return None
