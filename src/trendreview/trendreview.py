# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 14:58:18 2021

@author: jvorsten
"""

# Python imports
import argparse
import os
import sys

# Third party imports

# Local imports
from trendreview.ddvav import DDVAVRules
from trendreview.GraphAll import GraphAll
from trendreview.reporting import FDDImageGeneration, FDDReporting
from trendreview.FDDExceptions import FDDException

# Declarations
SUPPORTED_EQUIPMENT = ['ddvav', 'GraphAll', 'GraphMultipleAgainstDependentAxis']
description = """
Fault Diagnostics and Detection for trend review of mechanical equipment
"""
DESCRIPTION_GRAPH_COLUMNS = """
When combined with the 'GraphAll' option:
Only graph the specified columns on the dependent axis when 
using the "GraphAll" option. Specify column header names with 
a space between each name. To graph all columns then omit this argument.

When combined with the 'GraphMultipleAgainstDependentAxis' option:
Graph the specificed columns on a SINGLE graph. This will plot two (or more)
dependent variables against a single independent variable (for example, DateTime)
"""
DESCRIPTION_SUPPORTED_EQUIPMENT = f"""
Type of mechanical equipment being trended. Must
be one of {SUPPORTED_EQUIPMENT}. Use GraphAll to create a graph of every
data column versus the primary axis (default: DateTime).
Use 'GraphMultipleAgainstDependentAxis' to create a  graph of two or more
data columns versus the primary axis (default: DateTime)
"""
parser = argparse.ArgumentParser(description=description)
parser.add_argument('--filepath', '-f', type=os.path.abspath,
                    required=True, dest='filepath',
                    help='file path to trended data in CSV format')
parser.add_argument('--type', '-t', type=str,
                    choices=SUPPORTED_EQUIPMENT, required=True,
                    dest='type',
                    help=DESCRIPTION_SUPPORTED_EQUIPMENT)
parser.add_argument('--report-path', type=argparse.FileType('w', encoding='utf-8'),
                    required=False, default='./report.txt',
                    dest='log_filepath',
                    help='Filename to save report, like c:/path/to/report.txt')
parser.add_argument('--datetime-header', type=str,
                    required=False, dest='independent_axis_name',
                    help=('Header label of independent axis used to graph data ' +
                          'against. Use to override default value of "DateTime".'),
                    default='DateTime')
parser.add_argument('--graph-columns', type=str, action='extend', nargs='+',
                    dest='graph_columns', default=None,
                    required=False, help=DESCRIPTION_GRAPH_COLUMNS)

# %%


def main(parser: argparse.ArgumentParser):
    """Entrypoint
    Parse user arguments and being based on arguments"""
    # Parse arguments
    namespace = parser.parse_args()
    filepath = os.path.abspath(namespace.filepath)
    equipment_type = namespace.type
    log_filepath = os.path.abspath(namespace.log_filepath.name)
    namespace.log_filepath.close()
    independent_axis_name = namespace.independent_axis_name
    graph_columns = namespace.graph_columns  # List

    # Review data and run report
    reporter = FDDReporting(log_filepath=log_filepath)

    # Apply fault detection rules for dual duct terminal unit and create report
    if equipment_type == 'ddvav':
        ddvavRules = DDVAVRules(filepath)
        methods = ddvavRules.get_rules()
        for method in methods:
            try:
                method(ddvavRules.data)
            except FDDException as e:
                reporter.log_exception(e, create_image=True)

    # Do not apply fault detection rules for any equipment
    # Create report and graph all data versus 'DateTime'
    elif equipment_type == 'GraphAll':
        # Possilbe configuration in the future
        dependent_axis_names = graph_columns  # List of names
        # Load data
        graphall = GraphAll(filepath, parse_dates=independent_axis_name)
        graphall.graph_all_data(
            reporter, independent_axis_name, dependent_axis_names)
        
    elif equipment_type == 'GraphMultipleAgainstDependentAxis':
        # Graph multiple dependent axis data against the independent axis (DateTime)
        dependent_axis_names = graph_columns  # List of names
        
        # Chart properties defined for a scatter plot
        chart_properties = {
            'dash_capstyle': 'butt',  # Doesn't matter with scatter
            'marker': '.',  # point, could also try pixel depending on amount of data
            'markersize': 2,  # points, diameter or marker
            'markevery': None,  # Plot all markers
            'linestyle': 'None',
        }
        graphall = GraphAll(filepath, parse_dates=independent_axis_name)
        graphall.graph_multiple_dependent_axis(
            reporter, independent_axis_name, 
            dependent_axis_names=graph_columns, chart_properties=chart_properties
        )

    return None


if __name__ == '__main__':
    sys.exit(main(parser))
