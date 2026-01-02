# encoding UTF-8
# pylint: disable=C0103:invalid-name
"""
Created 2025-12-30 by John Vorsten

This module has a set of functions used to automate trendreview graphing on data saved 
in an inconvenient way.
This module was made to save time and work around manual transforming of data.

Given a .csv file which has multiple data oriented in 'list' format, graph each data 
against its primary key

Usage instructions:
-------
Activate a python environment with trendreview installed
    (like ./venv/scripts/activate.ps1)
Change directory to ./src so you can execute this script as a module
Command line arguments need to be entered
python -m scripts.automate_graphing_with_multiple_primarykey --input-file c:/path/to/inputfile.csv


Example:
-------
with an input .csv file like:

# pylint: disable=C0301:line-too-long
DateTime,value1,DateTime,value2,DateTime,value3,DateTime,value4
2025-12-09 18:45,68.28,2025-12-09 16:15,39,2025-12-09 21:28,68,2025-12-09 17:45,60.22399902
2025-12-09 20:00,68.07,2025-12-09 18:45,45,2025-12-09 23:41,72,2025-12-09 21:00,66.41600037
2025-12-09 22:00,72.28,2025-12-09 20:00,47,2025-12-10 4:30,72,2025-12-10 0:00,58.71199799
2025-12-10 3:15,71.92,2025-12-10 1:15,43,2025-12-10 11:49,68,2025-12-10 1:45,61.15999603

(transformed to a readable format)
DateTime            |value1	|DateTime	        |value2	|DateTime	        |value3	|DateTime	        |value4
2025-12-09 18:45	|68.28	|2025-12-09 16:15	|39	    |2025-12-09 21:28	|68	    |2025-12-09 17:45	|60.22399902
2025-12-09 20:00	|68.07	|2025-12-09 18:45	|45	    |2025-12-09 23:41	|72	    |2025-12-09 21:00	|66.41600037
2025-12-09 22:00	|72.28	|2025-12-09 20:00	|47	    |2025-12-10 4:30	|72	    |2025-12-10 0:00	|58.71199799
2025-12-10 3:15	    |71.92	|2025-12-10 1:15	|43	    |2025-12-10 11:49	|68	    |2025-12-1 01:45	|61.15999603

Graph each column 'value' against the corresponding 'DateTime' primary key

Assumptions
------
- Each column named 'DateTime' is the primary key
- Each column named 'DateTime' has a corresponding value in the next column
- Each data under 'DateTime' might be different than other DateTime columns
- Each DateTime is readable by the Trendreview package.

# pylint: enable=C0301:line-too-long
"""
# Python imports
from __future__ import annotations
from argparse import ArgumentParser, Namespace
import os
import glob
from pathlib import Path
from csv import reader
from typing import List, Optional, Dict, Any, Callable
from datetime import datetime
import re

# Third party imports

# Local imports
from trendreview.reporting import FDDImageGeneration
from trendreview.FDDExceptions import FDDException

# Declarations
USERPROFILE_PATH = str(os.environ.get('USERPROFILE'))
BASE_DIR = os.path.join(USERPROFILE_PATH, *['downloads'])
FILENAMES = glob.glob(os.path.join(BASE_DIR, '*.csv'))
PRIMARY_KEY_COLUMN:str = "DateTime"
GRAPH_DATA_LIST:List[Dict] = []
DATA_DICTIONARY = Dict[str, Dict[str, List[str]]]
CHART_PROPERTIES = {
    'dash_capstyle': 'butt',  # Doesn't matter with scatter
    'marker': '.',  # point, could also try pixel depending on amount of data
    'markersize': 2,  # points, diameter or marker
    'markevery': None,  # Plot all markers
    'linestyle': 'None',
}
PreferredType = str  # one of: "integer", "float", "text", "date", "boolean"

#%%

def main_setup_args() -> Namespace:
    """Gather command line arguments from the user

    Returns:
        _type_: _description_
    """
    DEFAULT_REPORT_FILENAME = 'report.txt'
    parser = ArgumentParser(description="Input .csv file path to be graphed")
    parser.add_argument('-i', '--input-file', type=str, required=True,
                        help='Input csv file to be cleaned')

    args = parser.parse_args()
    args.report_path = os.path.join(os.path.dirname(args.input_file), DEFAULT_REPORT_FILENAME)
    args.PRIMARY_KEYS_COLUMN = 'DateTime'

    return args


def get_dict_of_primary_key_values(header_row:List[str]) -> DATA_DICTIONARY:
    """_summary_

    Args:
        header_row (List[str]): a list of strings like 
        [DateTime,value1,DateTime,value2,DateTime,value3]

    Returns:
        Dict[str, Dict[str, List]]: dictionary containing the csv data like
        {'value1':{
            'values':['1','2','3','4'],
            'DateTime':['2025-12-30T11:20:30', '2025-12-30T11:25:30', '2025-12-30T11:30:30',]
            }
        }
    """
    data_dictionary:DATA_DICTIONARY = {}
    
    if len(header_row) % 2 != 0:
        msg="The number of header columns in the passed file is not even. \
            Each DateTime column must have a value column paired with it."
        raise ValueError(msg)
    
    for index in range(len(header_row) // 2):
        expected_datetime_header = header_row[index*2]
        value_name = header_row[index*2+1]
        
        if expected_datetime_header != 'DateTime':
            print(expected_datetime_header)
            print(type(expected_datetime_header))
            print(repr(expected_datetime_header), repr('DateTime'))
            print(list(map(ord, expected_datetime_header)), list(map(ord, 'DateTime')))  # show code points

            msg = (f"Expected the column header '{expected_datetime_header}' to be 'DateTime'. The\
                CSV file may not be formatted correctly")
            raise ValueError(msg)
        data_dictionary[value_name] = {'DateTime':[],
                                       'values':[]}
    return data_dictionary


def insert_data_to_data_dictionary(data_dictionary:DATA_DICTIONARY, row:List[str], n_columns:int, value_headers:List[str]) -> None:
    """
    Args:
        data_dictionary (DATA_DICTIONARY): _description_

    Returns:
        _type_: _description_
    """
    # Columns are assumed to be paired ['DateTime','value1','DateTime','value2',...]
    for index in range(n_columns // 2):
        data_dictionary[value_headers[index]]['DateTime'].append(row[index*2])
        data_dictionary[value_headers[index]]['values'].append(row[index*2+1])
    
    return None


def choose_preferred_dtype(
    values: List[str],
    *,
    allow_missing: bool = True,
    missing_values: Optional[List[str]] = None,
    thousands: Optional[str] = None,     # e.g., "," for "1,234"
    decimal: str = ".",                  # "." or ","
    date_formats: Optional[List[str]] = None,
    boolean_true: Optional[List[str]] = None,
    boolean_false: Optional[List[str]] = None,
) -> PreferredType:
    """
    Decide the preferred data type for a list of strings.
    Returns one of: "integer", "float", "text", "date", "boolean".

    Parameters
    ----------
    values : list of str
        Raw string values to evaluate.
    allow_missing : bool
        If True, ignores missing-like tokens during type checks.
    missing_values : list of str
        Tokens considered missing. Default includes "", "NA", "N/A", "NaN", "null", "None", " " (whitespace).
    thousands : str or None
        Character used as thousands separator (e.g., ","). If provided, it will be stripped for numeric checks.
    decimal : str
        Decimal separator. Use "," to support e.g., "1.234,56".
    date_formats : list of str or None
        Formats to try with datetime.strptime. If None, a common set is used.
    boolean_true / boolean_false : list of str or None
        Tokens recognized as booleans (case-insensitive). Defaults include typical variants.

    Notes
    -----
    - The detection order is: boolean → integer → float → date → text.
    - Numeric detection supports localized separators if `thousands` and `decimal` are specified.
    - Date detection tries multiple common formats; if you need more flexibility, add formats.
    """

    # ---------- Defaults ----------
    if missing_values is None:
        missing_values = ["", "NA", "N/A", "NaN", "null", "None"]
    # treat whitespace-only as missing too
    missing_values = [m.lower() for m in missing_values] + [" "]

    if boolean_true is None:
        boolean_true = ["true", "t", "yes", "y", "1"]
    if boolean_false is None:
        boolean_false = ["false", "f", "no", "n", "0"]

    # Common date formats (extend as needed)
    if date_formats is None:
        date_formats = [
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%m-%d-%Y",
            "%Y/%m/%d",
            "%d/%m/%Y",
            "%m/%d/%Y",
            "%Y.%m.%d",
            "%d.%m.%Y",
            "%m.%d.%Y",
            "%Y%m%d",
            "%d %b %Y",   # 30 Dec 2025
            "%d %B %Y",   # 30 December 2025
            "%b %d, %Y",  # Dec 30, 2025
            "%B %d, %Y",  # December 30, 2025
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%d %H:%M",
        ]

    # ---------- Helpers ----------
    def is_missing(s: str) -> bool:
        return s.strip() == "" or s.strip().lower() in missing_values

    def normalize_numeric_token(s: str) -> str:
        """
        Remove thousands separator and normalize decimal.
        If decimal is ',', convert to '.' for float parsing.
        """
        t = s.strip()
        if thousands:
            t = t.replace(thousands, "")
        if decimal == ",":
            # make sure only the last comma is the decimal if multiple are present
            # a simple approach: replace the last comma with dot, others stay (often grouping marks)
            if t.count(",") == 1:
                t = t.replace(",", ".")
            else:
                # If both '.' and ',' exist, assume '.' are thousands and last ',' is decimal
                # Replace all '.' (grouping) then last ',' to '.'
                t = t.replace(".", "")
                last_comma = t.rfind(",")
                if last_comma != -1:
                    t = t[:last_comma] + "." + t[last_comma+1:]
        return t

    def is_boolean(s: str) -> bool:
        t = s.strip().lower()
        return t in boolean_true or t in boolean_false

    def is_integer(s: str) -> bool:
        t = normalize_numeric_token(s)
        # Only digits with optional leading sign
        return bool(re.fullmatch(r"[+-]?\d+", t))

    def is_float(s: str) -> bool:
        t = normalize_numeric_token(s)
        # Accept integers as floats also
        # Accept decimal numbers, scientific notation
        res = bool(re.fullmatch(r"[+-]?(\d+\.\d+|\d+\.|\.\d+|\d+)([eE][+-]?\d+)?", t))
        return res

    def is_date(s: str) -> bool:
        t = s.strip()
        for fmt in date_formats:
            try:
                datetime.strptime(t, fmt)
                return True
            except ValueError:
                continue
        return False

    # ---------- Filter values ----------
    checked = []
    for v in values:
        if allow_missing and is_missing(v):
            # Done append missing values to the list to be checked
            continue
        checked.append(v)

    # If all values are missing/empty, default to text
    if len(checked) == 0:
        return "text"

    # ---------- Detection in order ----------
    is_float_check = [is_float(v) for v in checked]
    if all(is_boolean(v) for v in checked):
        return "boolean"
    if all(is_integer(v) for v in checked):
        return "integer"
    if all(is_float_check):
        return "float"
    if all(is_date(v) for v in checked):
        return "date"
    return "text"


def cast_list(
    values: List[str],
    target: str,  # one of: "integer", "float", "boolean", "date", "text"
    *,
    missing_values: Optional[List[str]] = None,
    thousands: Optional[str] = None,  # e.g., "," for "1,234"
    decimal: str = ".",               # "." or ","
    date_formats: Optional[List[str]] = None,
    boolean_true: Optional[List[str]] = None,
    boolean_false: Optional[List[str]] = None,
    strip_whitespace: bool = True,
) -> List[Any]:
    """
    Cast a list of strings to a specific data type.
    Returns a list of Python values or None for items that cannot be converted.

    target:
        "integer"  -> int (nullable -> None for invalid/missing)
        "float"    -> float (nullable)
        "boolean"  -> bool (nullable)
        "date"     -> datetime (nullable)
        "text"     -> str (original or stripped)
    """

    # ---------- Defaults ----------
    if missing_values is None:
        missing_values = ["", "NA", "N/A", "NaN", "null", "None"]

    if boolean_true is None:
        boolean_true = ["true", "t", "yes", "y", "1"]
    if boolean_false is None:
        boolean_false = ["false", "f", "no", "n", "0"]

    if date_formats is None:
        date_formats = [
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%m-%d-%Y",
            "%Y/%m/%d",
            "%d/%m/%Y",
            "%m/%d/%Y",
            "%Y.%m.%d",
            "%d.%m.%Y",
            "%m.%d.%Y",
            "%Y%m%d",
            "%d %b %Y",
            "%d %B %Y",
            "%b %d, %Y",
            "%B %d, %Y",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%d %H:%M",
        ]

    missing_set = {m.lower() for m in missing_values}

    # ---------- Helpers ----------
    def is_missing(s: str) -> bool:
        t = s.strip() if strip_whitespace else s
        return t == "" or t.lower() in missing_set

    def norm_num(s: str) -> str:
        """
        Normalize numeric string:
        - remove thousands separator
        - convert decimal ',' to '.' when requested
        """
        t = s.strip() if strip_whitespace else s
        if thousands:
            t = t.replace(thousands, "")
        if decimal == ",":
            # handle cases with both '.' and ','
            if t.count(",") == 1 and "." not in t:
                t = t.replace(",", ".")
            else:
                # remove all '.' (assume grouping) and make last ',' the decimal
                t = t.replace(".", "")
                idx = t.rfind(",")
                if idx != -1:
                    t = t[:idx] + "." + t[idx+1:]
        return t

    def to_int(s: str) -> Optional[int]:
        if is_missing(s):
            return None
        t = norm_num(s)
        # Accept only integer forms (sign + digits)
        if re.fullmatch(r"[+-]?\d+", t):
            try:
                return int(t)
            except ValueError:
                return None
        return None

    def to_float(s: str) -> Optional[float]:
        if is_missing(s):
            return None
        t = norm_num(s)
        # Accept integers or decimals, optional scientific notation
        if re.fullmatch(r"[+-]?(\d+(\.\d+)?|\.\d+)([eE][+-]?\d+)?", t):
            try:
                return float(t)
            except ValueError:
                return None
        return None

    def to_bool(s: str) -> Optional[bool]:
        if is_missing(s):
            return None
        t = s.strip().lower() if strip_whitespace else s.lower()
        if t in boolean_true:
            return True
        if t in boolean_false:
            return False
        return None

    def to_date(s: str) -> Optional[datetime]:
        if is_missing(s):
            return None
        t = s.strip() if strip_whitespace else s
        for fmt in date_formats:
            try:
                return datetime.strptime(t, fmt)
            except ValueError:
                continue
        return None

    def to_text(s: str) -> str:
        return s.strip() if strip_whitespace else s

    # ---------- Dispatcher ----------
    converters: dict[str, Callable[[str], Any]] = {
        "integer": to_int,
        "float": to_float,
        "boolean": to_bool,
        "date": to_date,
        "text": to_text,
    }
    target = target.lower()
    if target not in converters:
        raise ValueError(f"Unsupported target '{target}'. Use one of: {list(converters.keys())}")

    conv = converters[target]
    return [conv(v) for v in values]


def main(args:Namespace):
    
    # First, read the data from the csv file into a dictionary
    with open(args.input_file, encoding='utf-8') as csvfile:
        csvreader = reader(csvfile, delimiter=',')
        # First deal with the header row
        header_row = next(csvreader)
        data_dictionary = get_dict_of_primary_key_values(header_row)
        n_columns:int = len(header_row)
        value_headers = list(data_dictionary.keys())
        
        for row in csvreader:
            # Next, read each row from the csv file and save them into a list of dictionaries
            insert_data_to_data_dictionary(data_dictionary, row, n_columns, value_headers)
        
        # Next, create a graph for each variable
        image_generator = FDDImageGeneration(os.path.dirname(args.input_file))
        for key, value in data_dictionary.items():
            preferred_dtype = choose_preferred_dtype(
                value['values'], allow_missing=True, 
                )
            values = cast_list(value['values'], preferred_dtype)
            datetimes = cast_list(value['DateTime'], 'date')
            FDD_dictionary = {
                'primary_axis_label':'DateTime',
                'dependent_axis_labels':[key],
                key:values,
                'DateTime':datetimes,
                    }
            msg = f"graphing DateTime versus {key}"
            exception = FDDException(msg, FDD_dictionary)
            image = image_generator.generate_image(exception, CHART_PROPERTIES)
            image_generator.save_image(image)
            
    return None

if __name__ == '__main__':
    main(main_setup_args())