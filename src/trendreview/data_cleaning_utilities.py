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
from typing import List, Callable
import os

# Third party imports

# Local imports

# Declarations
DEFAULT_OUTPUT_CSV = 'clean_csv.csv'

# Rules for line deletion

# %%

def _is_line_empty(line: List[str]) -> bool:
    """A line is empty if all text within the row is empty
    Return True fi all text within the line is empty"""
    for text in line:
        if text == '':
            continue
        else:
            return False
    return True

def _is_any_text_empty(line: List[str]) -> bool:
    """A text is empty if it equals an empty string ''
    Assume that if any line contains an empty entry then the data on this
    line is corrupted
    Return True if any text is empty within the line"""

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

def _replace_empty_with_previous_value(line: List[str], previous_line: List[str]) -> List[str]:
    """Given a line of text, determine if there are empty fields. If so, then replace
    the empty fields with the value of the previous line"""
    for index, text in enumerate(line):
        if text == '':
            # Replace value with previous line
            line[index] = previous_line[index]
        else:
            pass

    return line

def main(input_filepath: str, *filters:Callable, output_filepath:str=None) -> None:
    """Main function for data filtering operations
    Example
    -------
    from data_cleaning_utilities import _is_line_empty, _is_number_of_colmns_match_header_columns, _is_any_text_empty

    def custom_filter_factory_function(line: List[str]):
        n_headers = 6 # We expect 6 header columns
        return _is_number_of_colmns_match_header_columns(line, n_headers)

    filters = [_is_line_empty, custom_filter_factory_function, _is_any_text_empty]
    input_filepath = './path/to/input_file.csv'
    output_filepath = './path/to/output_file.csv'
    main(input_filepath, filters, output_filepath)

    """
    output_filepath = os.path.join(os.path.dirname(input_filepath), DEFAULT_OUTPUT_CSV)

    with open(input_filepath, 'rt', encoding='UTF-8') as input_file, \
            open(output_filepath, 'wt', encoding='UTF-8', newline='') as output_file:
        # Iterate line by line
        reader = csv.reader(input_file, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer = csv.writer(output_file, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)

        row: List[str]
        for row in reader:
            # Filter out rows based on the input filters passed
            for filter_func in filters:
                if filter_func(row):
                    # If the filter evaluates to true then we do not want the line anymore
                    # Do not write it to the clean file
                    pass
                else:
                    writer.writerow(row)

    return None
