# encoding UTF-8
"""
Created 2022-5-26

Remove bad lines from a .csv file based on a set of rules
1. If a line contains no data, then remove the line
2. This data contains higher than 5% alphabetic characters. If the data is highly (greater than 5%)
word characters then remove the line

Replace empty data within a csv file with data from the previous line

Lines are read from an existing .csv file, and written to a new file if the line passes
both rules listed. This script does NOT check for headers

author John Vorsten
"""

# Python imports
import csv
from typing import List
from argparse import ArgumentParser
from pathlib import Path
import os
from copy import deepcopy

# Third party imports

# Local imports
from scripts.data_cleaning_utilities import _fill_empty_line_with_previous_data, _is_line_primarily_numeric, _is_line_empty

# Declarations
DEFAULT_OUTPUT_CSV = 'clean_csv.csv'
parser = ArgumentParser(description="Input .csv file path to be cleaned")
parser.add_argument('-i', '--input-file', type=str, required=True,
                    help='Input csv file to be cleaned')
parser.add_argument('-o', '--output-file',
                    type=Path, required=False,
                    help="Output file name or path")
parser.add_argument('-a', '--filter-alphabetic', type=bool, required=False,
                    default=False,
                    help="Filter out Alphabetic lines which contain alphabetic characters. \
                        If a line contains greater than 5% of alphabetic characters then remove the line.")
parser.add_argument('--replace-empty-line-with-previous-data', type=bool, required=False,
                    default=False,
                    help="If a line contains empty strings then replace the empty string with data from the prevous line")
parser.add_argument('--remove-empty-line', required=False, type=bool,
                    default=False,
                    help="If a line starts with an empty string then remove the line entirely")
args = parser.parse_args()
INPUT_CSV = args.input_file
if args.output_file:
    OUTPUT_CSV = args.output_file
else:
    OUTPUT_CSV = os.path.join(os.path.dirname(
        args.input_file), DEFAULT_OUTPUT_CSV)

# Rules to be enforced on parser arguments
if args.filter_alphabetic == True and any((args.replace_empty_line_with_previous_data == True, args.remove_empty_line == True)):
    msg: str = "You can only choose to set ONE of the arguments [--filter-alphabetic, --replace-empty-line-with-previous-data, --remove-empty-line] to True"
    print(msg)
    exit(1)

if args.replace_empty_line_with_previous_data == True and any((args.filter_alphabetic == True, args.remove_empty_line == True)):
    msg: str = "You can only choose to set ONE of the arguments [--filter-alphabetic, --replace-empty-line-with-previous-data, --remove-empty-line] to True"
    print(msg)
    exit(1)

if args.remove_empty_line == True and any((args.filter_alphabetic == True, args.replace_empty_line_with_previous_data == True)):
    msg: str = "You can only choose to set ONE of the arguments [--filter-alphabetic, --replace-empty-line-with-previous-data, --remove-empty-line] to True"
    print(msg)
    exit(1)

# %%


def main():
    """Read a .csv file and write valid lines to a new file
    Lines are invalid if:
    1. If a line contains no data, then remove the line
    2. This data is primarily numeric. If the data is primarily (greater than 5%)
    word characters then remove the line
    """

    with open(INPUT_CSV, 'rt', encoding='UTF-8') as input_file, \
            open(OUTPUT_CSV, 'wt', encoding='UTF-8', newline='') as output_file:
        # Iterate line by line
        reader = csv.reader(input_file, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer = csv.writer(output_file, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Intialize the first read row and the previous row. The first row is the header row
        row: List[str] = next(reader)
        previous_row: List[str] = deepcopy(row)
        writer.writerow(row) # Write the header to the new file

        for row in reader:

            # Filter out empty rows and rows which contain more than 5% alphabetic characters
            if args.filter_alphabetic:
                if _is_line_primarily_numeric(row):
                    writer.writerow(row)
                    continue  # Can only evaluate this rule once per line
                else:
                    pass  # Do not write lines with lots of alphabetic characters

            if args.replace_empty_line_with_previous_data:
                _fill_empty_line_with_previous_data(
                    new_row=row, previous_row=previous_row)
                writer.writerow(row)
                previous_row = deepcopy(row)
                continue

            if args.remove_empty_line:
                if _is_line_empty(row):
                    pass  # Do not write empty lines
                else:
                    writer.writerow(row)
                    continue

    return None


if __name__ == '__main__':
    main()
