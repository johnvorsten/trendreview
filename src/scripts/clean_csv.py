# encoding UTF-8
"""
Created 2022-5-26

Remove bad lines from a .csv file based on a set of rules
1. If a line contains no data, then remove the line
2. This data contains higher than 5% alphabetic characters. If the data is highly (greater than 5%)
word characters then remove the line

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

# Third party imports

# Local imports

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
                    help="Filter out Alphabetic lines which contain alphabetic characters")
args = parser.parse_args()
INPUT_CSV = args.input_file
if args.output_file:
    OUTPUT_CSV = args.output_file
else:
    OUTPUT_CSV = os.path.join(os.path.dirname(args.input_file), DEFAULT_OUTPUT_CSV)

# Rules for line deletion

# %%

def _is_line_empty(line: List[str]) -> bool:
    """A line is empty if its first entry contains an empty string ''"""
    if line[0] != '':
        return False

    return True

def _is_any_text_empty(line: List[str]) -> bool:
    """A text is empty if it equals an empty string ''
    Assume that if any line contains an empty entry then the data on this
    line is corrupted"""

    for text in line:
        if text == '':
            return True

    return False

def _is_line_primarily_numeric(line: List[str], threshold: float = 0.05) -> bool:
    """Determine if the majority of characters on a line are numeric
    If the default threshold of 5% alphabetic characters is exceeded then
    the line is considered to not be primarily numeric"""
    n_numeric: int = 0
    n_alphabetic: int = 0

    for text in line:
        if text.replace('.', '', 1).isnumeric():
            n_numeric += 1
        elif text.isalpha():
            n_alphabetic += 1

    if n_alphabetic + n_numeric == 0:
        return False
    elif len(line) == 0:
        return False
    elif n_alphabetic / (n_alphabetic + n_numeric) >= threshold:
        return False
    else:
        return True

def _is_number_of_colmns_match_header_columns(line: List[str], n_headers: int) -> bool:
    """Determine if the number of data columns matches the number of header columns.
    If a line contains empty entries we can assume that the line is not valid"""
    n_empty: int = 0
    n_not_empty: int = 0

    for text in line:
        if text != '':
            n_not_empty += 1
        else:
            n_empty += 1

    if n_not_empty != n_headers:
        return False

    return True

def _filter1(row: List[str]) -> bool:
    """Filter1 determines if a row either contains empty columns OR
    if the row is primarily numeric (greater than 95% numeric characters default)"""

    if any((_is_any_text_empty(row), not _is_line_primarily_numeric(row))):
        return True

    return False

def _filter2(row: List[str]) -> bool:
    """Filter2 determines if a row either contains empty columns"""

    if _is_any_text_empty(row):
        return True

    return False

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

        row: List[str]
        for row in reader:
            # Filter out empty rows and rows which contain more than 5% alphabetic characters
            if args.filter_alphabetic:
                if _filter1(row):
                    pass
                else:
                    writer.writerow(row)
            # Only filter out lines containing empty columns
            else:
                if _filter2(row):
                    pass
                else:
                    writer.writerow(row)

    return None


if __name__ == '__main__':
    main()
