# encoding UTF-8
"""
Created 2022-5-26

Remove bad lines from a .csv file based on a set of rules
1. If a line contains no data, then remove the line
2. This data is primarily numeric. If the data is primarily (greater than 5%)
word characters then remove the line

Lines are read from an existing .csv file, and written to a new file if the line passes
both rules listed. This script does NOT check for headers

author John Vorsten
"""

# Python imports
import csv
from typing import List

# Third party imports

# Local imports

# Declarations
OUTPUT_CSV = r"N:\hou\2021\21934-00\60 Commissioning\06 Submittals & Submittal Reviews\ACB_vault2_trend_clean.csv"
INPUT_CSV = r"N:\hou\2021\21934-00\60 Commissioning\06 Submittals & Submittal Reviews\ACB_vault2_trend.csv"
# Rules for line deletion

# %%


def _is_line_empty(line: List[str]):

    for text in line:
        if text != '':
            return False

    return True


def _is_line_primarily_numeric(line: List[str], threshold: float = 0.05):
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
            if any((_is_line_empty(row), not _is_line_primarily_numeric(row))):
                pass
            else:
                writer.writerow(row)

    return None

if __name__ == '__main__':
    main()
