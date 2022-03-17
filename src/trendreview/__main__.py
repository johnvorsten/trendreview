# Python imports
import argparse
import os

# Third party imports

# Local imports
from .ddvav import DDVAVRules
from .GraphAll import GraphAll
from .reporting import FDDImageGeneration, FDDReporting
from .FDDExceptions import FDDException

# Declarations
SUPPORTED_EQUIPMENT = ['ddvav', 'GraphAll']
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
                    'be one of {}. Use GraphAll to create a graph of every '+
                    'data column versus the primary axis (DateTime)'.format(SUPPORTED_EQUIPMENT)))
parser.add_argument('--report-path', type=argparse.FileType('w', encoding='utf-8'),
                    required=False, default='./report.txt',
                    dest='log_filepath',
                    help='Filename to save report, like c:/path/to/report.txt')

#%%

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
        ddvavRules = DDVAVRules(filepath)
        methods = ddvavRules.get_rules()
        for method in methods:
            try:
                method(ddvavRules.data)
            except FDDException as e:
                reporter.log_exception(e, create_image=True)
                
    if equipment_type == 'GraphAll':
        # Possilbe configuration in the future
        independent_axis_name = 'DateTime'
        dependent_axis_names = None # Graph all
        # Load data
        graphall = GraphAll(filepath)
        graphall.graph_all_data(reporter, independent_axis_name, dependent_axis_names)