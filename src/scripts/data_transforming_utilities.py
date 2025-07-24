# encoding UTF-8
"""_summary_
Created 2025-7-23 by John Vorsten

This module has a set of functions used for transforming and re-organizing data

Given a .csv file which is oriented in a 'dictionary' format, convert the file to a 'list' oriented format | 
using a certain column as the primary key, a column for headers, and a header for values
Example:
-------
with an input .csv file like:

index,name,customer_group,DateTime,value,units
1,jonathan query,88,2022-12-12T00:00Z,78.2,dollars
2,abagail longshore,88,2022-12-12T00:00Z,0,dollars
3,Emilia Erhardt,88,2022-12-12T00:00Z,0.1,dollars
4,Joaquin Burquis,88,2022-12-12T00:00Z,76.1,cents

(transformed to a readable format)
index  |name               |cutomer_group |DateTime           |value  |units
1      |jonathan query     |88            |2022-12-12T00:00Z  |78.2   |dollars
2      |abagail longshore  |88            |2022-12-12T00:00Z  |0      |dollars
3      |Emilia Erhardt     |88            |2022-12-12T00:00Z  |0.1    |dollars
4      |Joaquin Burquis    |88            |2022-12-12T00:00Z  |76.1   |cents

Transform the file with DateTime as the primary key, with the 'name' column providing the headers, and the 'value' column providing data on each record
DateTime,jonathan query,abagail longshore,Emilia Erhardt,Joaquin Burquis
2022-12-12T00:00Z,78.2,0.0,0.1,76.1

(transformed to a readable format)
DateTime            |jonathan query|abagail longshore|Emilia Erhardt|Joaquin Burquis
2022-12-12T00:00Z   |78.2          |0.0              |0.1           |76.1
"""

# Python imports
import os
import csv
import glob
from typing import List, AbstractSet, Set, Any, Tuple
from argparse import ArgumentParser
from pathlib import Path
from copy import deepcopy

# Third party imports
import pandas as pd

# Local imports

# Declarations
USERPROFILE_PATH = str(os.environ.get('USERPROFILE'))
BASE_DIR = os.path.join(USERPROFILE_PATH, *['downloads', 'csv_transpose'])
FILENAMES = glob.glob(os.path.join(BASE_DIR, '*.csv'))
PRIMARY_KEY_COLUMN:str = "DateTime"
HEADERS_COLMUN:str = "Description"
VALUES_COLUMN:str = "Value"
TRANSFORM_DICTIONARY = dict[str, dict[str, Any]]
"""{primary_key_1: {header_1:value, header_2:value, ..., header_n:value}, 
    primary_key_2: {...},
    }"""

# %%

def get_list_header_names(headers: List[str]) -> List[str]:
    """Return a list of header names which have been cleaned
    There is no cleaning requirement for header names at this time
    This function is redundant, but remains for future use"""
    clean_headers: List[str] = []
    for idx in range(1, len(headers)):
        clean_headers.append((headers[idx]))
    return clean_headers

def get_unique_header_names_on_existing_data(header_names_list:List[str]) -> Set[str]:
    """Create a set of unique strings from a list of strings
    inputs
    ------
    header_names_list List[str]: A list of strings
    outputs
    -------
    Set[str]: A set of strings
    """
    unique_header_names: Set[str] = set()
    unique_header_names = set(header_names_list)
    return unique_header_names

def get_unique_primary_keys_on_existing_data(primary_keys_list:List[str]) -> Set[str]:
    """Output a set of unique primary keys from a list of strings
    inputs
    -------
    
    outputs
    -------
    
    It is common to get data which is oriented with NO UNIQUE primary key.
    For example, data is sampled at uniform time intervals of 5 minutes. 
    There are multiple data points sampled in a trend, in this case temperature, humidity, and sun intensity.
    Each data point is logically associated with a time (like 2025-7-23 at 6:15:20.00 PM).
    The data points are not sampled at exact unique intervals, so temperature might be logged at 
    6:15:20.00 and humidity might be logged at 6:15:21.63"""
    
    unique_primary_keys: Set[str]
    unique_primary_keys = set(primary_keys_list)
    return unique_primary_keys

def dictionary_factory_primary_keys(primary_keys_set:AbstractSet[str], unique_headers_set:AbstractSet[str]) -> TRANSFORM_DICTIONARY:
    """Create the specified dictionary with a unique set of primary keys"""
    primary_key_oriented_dictionary: TRANSFORM_DICTIONARY = {}
    columns_oriented_dictionary = dict.fromkeys(unique_headers_set)
    # Alternate method... primary_key_oriented_dictionary = dict.fromkeys(primary_keys_set)
    for primary_key in primary_keys_set:
        primary_key_oriented_dictionary[primary_key] = deepcopy(columns_oriented_dictionary)
    return primary_key_oriented_dictionary

def parse_csv_file(filename: str, headers_column:str, values_column:str, primary_key_column:str) -> Tuple[TRANSFORM_DICTIONARY, Set[str], Set[str]]:
    """
    1. Read a file path into a pandas dataframe
    2. Find a unique set of header names used from one of the columns in the input CSV file column data
    3. Find a unique set of primary keys from one of the columns in the input CSV file column data
    4. Create an output set of data where all data from the 'header data' is oriented on primary keys
    """
    # Read raw file into csv
    raw_df = pd.read_csv(filename)
    
    # 1. Create a unique set of column headers
    unique_header_names:Set[str] = get_unique_header_names_on_existing_data(raw_df.get(headers_column).to_list())
    
    # 2. Create a unique set of primary keys
    unique_primary_keys:Set[str] = get_unique_primary_keys_on_existing_data(raw_df.get(primary_key_column).to_list())
    
    # 3. Create a dictionary that will carry all of the columns, primary keys, and values in the format 
    # {primary_key_1: {header_1:value, header_2:value, ..., header_n:value}, 
    # primary_key_2: {...},
    # }
    transform_dictionary: TRANSFORM_DICTIONARY = dictionary_factory_primary_keys(unique_primary_keys, unique_header_names)

    for index, series in raw_df.iterrows():
        transform_dictionary[series.at[primary_key_column]][series.at[headers_column]] = series.at[values_column]

    return transform_dictionary, unique_header_names, unique_primary_keys

def write_csv_file(filename:str, transform_dictionary: TRANSFORM_DICTIONARY, headers:List[str]) -> None:
    """Write the entries in a dictionary to a .csv file format"""

    with open(filename, 'wt', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        row: List[Any] = []
        writer.writerow(headers)
        
        for primary_key_str, values_dict in transform_dictionary.items():
            row.append(primary_key_str)

            for value in values_dict.values():
                row.append(value)
            
            writer.writerow(row)
            row.clear()

    return None

def transform_csv(input_filepath:str, output_filepath:str, headers_column:str, values_column:str, primary_keys_column:str):
    """Transform the file with DateTime as the primary key, with the 'name' column providing the headers, and the 'value' column providing data on each record

    inputs
    -------
    input_filepath: path to file to be transformed
    headers_column: name of column which contains new header names
    values_column: name of column which contain data for each record
    primary_keys_column: name of column which contains the primary key for each record
    """

    transform_dictionary, unique_headers, _ = parse_csv_file(input_filepath, headers_column, values_column, primary_keys_column)
    headers_list:List[str] = list(unique_headers)
    headers_list.insert(0, primary_keys_column)
    write_csv_file(output_filepath, transform_dictionary, headers_list)

    return None

def main(args):
    """Execution steps:
    1. Create a unique set of primary keys
    2. Create a unique set of column headers
    3. Create a dictionary that will carry all of the columns, primary keys, and values in the format 
        {primary_key_1: {header_1:value, header_2:value, ..., header_n:value}, 
        primary_key_2: {...},
        }
    4. Write dictionary to .csv file
    """
    transform_dictionary, unique_headers, _ = parse_csv_file(args.input_file, args.headers_column, args.values_column, args.primary_keys_column)
    headers_list:List[str] = list(unique_headers)
    headers_list.insert(0, args.primary_keys_column)
    write_csv_file(args.output_file, transform_dictionary, headers_list)

    return None

def main_setup_args():

    DEFAULT_OUTPUT_CSV = 'clean_csv.csv'
    parser = ArgumentParser(description="Input .csv file path to be transformed")
    parser.add_argument('-i', '--input-file', type=str, required=True,
                        help='Input csv file to be cleaned')
    parser.add_argument('-o', '--output-file',
                        type=Path, required=False,
                        help="Output file name or path")
    parser.add_argument('-p', '--primary-keys-column', type=str, required=True,
                        help='Column name in old file which contains new primary keys')
    parser.add_argument('-c', '--headers-column', type=str, required=True,
                        help='Column name in old file which contains new column names')
    parser.add_argument('-v', '--values-column', type=str, required=True,
                        help='Column name in old file which contains new values')
    args = parser.parse_args()
    INPUT_CSV = args.input_file
    if args.output_file:
        pass
    else:
        args.output_file = os.path.join(os.path.dirname(args.input_file), DEFAULT_OUTPUT_CSV)

    return args

if __name__ == '__main__':
    args = main_setup_args()
    main(args)

