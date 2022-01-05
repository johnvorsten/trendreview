# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 14:58:18 2021

@author: jvorsten
"""

# Python imports
import argparse
import os

# Third party imports

# Local imports
from ddvav import DDVAVRules
from reporting import FDDImageGeneration, FDDReporting
from FDDExceptions import FDDException

# Declarations
SUPPORTED_EQUIPMENT = ['ddvav']
description = """Fault Diagnostics and Detection for trend review of mechanical 
equipment"""
parser = argparse.ArgumentParser(description=description)
parser.add_argument('--filepath', type=os.path.abspath,
                    required=True, dest='filepath',
                    help='file path to trended data in CSV format')
parser.add_argument('--type', type=str,
                    choices=SUPPORTED_EQUIPMENT, required=True,
                    dest='type',
                    help=('Type of mechanical equipment being trended. Must '+
                    'be one of {}'.format(SUPPORTED_EQUIPMENT)))
parser.add_argument('--report-path', type=argparse.FileType('w', encoding='utf-8'),
                    required=False, default='./report.txt',
                    dest='log_filepath',
                    help='Filename to save report, like c:/path/to/report.txt')


#%%


def test_parse_args():
    
    filepath = './data/DD03.csv'
    args = ['--filepath', filepath, '--type', 'ddvav']
    namespace = parser.parse_args(args)
    filepath = os.path.abspath(namespace.filepath)
    equipment_type = namespace.type
    log_filepath = os.path.abspath(namespace.log_filepath.name)
    namespace.log_filepath.close()
            
    return None



if __name__ == '__main__':
    # Parse arguments
    namespace = parser.parse_args()
    filepath = os.path.abspath(namespace.filepath)
    equipment_type = namespace.type
    log_filepath = os.path.abspath(namespace.log_filepath.name)
    namespace.log_filepath.close()
    
    # Review data and run report
    reporter = FDDReporting(log_filepath=log_filepath)
    if equipment_type == 'ddvav':
        try:
            DDVAVRules(filepath)
        except FDDException as e:
            reporter.log_exception(e, create_image=True)
    