"""Example
Create mapping from custom header titles to specific defined titles
Iteratively look through directory to find all .csv files for all equipment
Test specific cases for fan powered terminal unit

"""
# Python imports
from pathlib import Path
from typing import List
import configparser
import os
import sys

# Local imports
from trendreview.GraphAll import GraphAll
from trendreview.reporting import FDDReporting

# Third party imports

# Declarations
CONFIG_PATH = './examples/run_config.ini'
parser = configparser.ConfigParser()
parser.read(CONFIG_PATH, encoding=sys.getdefaultencoding())
type = parser['trendreview']['type']
base_directory = parser['trendreview']['base_directory']
report_path = parser['trendreview']['report_path']
datetime_header = parser['trendreview']['datetime_header']
graph_columns = parser['trendreview']['graph_columns']
INDEPENDENT_AXIS_NAME = datetime_header
DEPENDENT_AXIS_NAMES = graph_columns.split(',')

# %%


def gather_csv_filenames(search_directory: Path) -> List[str]:
    """Return all comma-separated files within a base directory"""
    return list(search_directory.glob('**/*.csv'))


def main() -> int:

    # Review data and run report
    log_filepath = os.path.abspath(report_path)
    reporter = FDDReporting(log_filepath=log_filepath)

    # Gather all .csv files within base directory
    filenames = gather_csv_filenames(Path(base_directory))

    # Iterate through files
    for filepath in filenames:
        graphall = GraphAll(filepath, parse_dates=datetime_header)
        graphall.graph_multiple_dependent_axis(
            reporter, INDEPENDENT_AXIS_NAME, DEPENDENT_AXIS_NAMES)

    return 0


if __name__ == '__main__':
    sys.exit(main())