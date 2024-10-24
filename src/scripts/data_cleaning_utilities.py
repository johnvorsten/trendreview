# encoding UTF-8
"""
Created 2024-10-22

This module contains data cleaning functions

Lines are read from an existing .csv file, and written to a new file.

author John Vorsten
"""

# Python imports
from typing import List


# Third party imports

# Local imports

# Declarations

# %%


def _fill_empty_line_with_previous_data(new_row: List[str], previous_row: List[str]) -> None:
    """Fill empty data with data from the previous row. Rows are modified in place."""
    # Iterate through all data in the new row and search for empty values
    for index, data in enumerate(new_row):
        if data == '':  # CSV files will always contain a list of strings
            new_row[index] = previous_row[index]

    return None

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
