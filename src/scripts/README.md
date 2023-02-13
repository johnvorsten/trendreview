## Usage instructions for scripts clean_csv.py

### Example input file located at /path/to/raw_csv.csv  

|Date     |Time     |Name         |Value  |Description |
|---------|---------|-------------|-------|------------|
|2023-1-2 |12:00:01 |Jinto Porchin|23.2   |A person    |
|         |12:00:03 |Missing data |       |            |
|2023-1-3 |12:00:02 |Blue         |255    |A color     |
|2023-1-4 |12:00:03 |Mocking bird |1      |A bird      |
|2023-1-5 |         |             |       |More missing data |

### Output file with command line arguments 
`python /src/scripts/clean_csv.py -i /path/to/raw_csv.csv -o /path/to/clean_csv.csv`

|Date     |Time     |Name         |Value  |Description |
|---------|---------|-------------|-------|------------|
|2023-1-2 |12:00:01 |Jinto Porchin|23.2   |A person    |
|2023-1-3 |12:00:02 |Blue         |255    |A color     |
|2023-1-4 |12:00:03 |Mocking bird |1      |A bird      |

## Usage from command line
```
>>> python src/scripts/clean_csv.py
usage: clean_csv.py [-h] -i INPUT_FILE [-o OUTPUT_FILE] [-a FILTER_ALPHABETIC]
clean_csv.py: error: the following arguments are required: -i/--input-file
```
command line arguments:  
* -i input file: Full pathname of input comma separated file. Example /path/to/raw_csv.py
* -o output file: Full pathname of output location to save cleaned .csv. Example /path/to/clean_csv.py. If no output pathname is specified, then the clean csv file is named 'clean_csv.csv' in the same directory as the input file.
* -a filter_alphabetic: Removes a row if a row contains greater than 5% alphabetic characters. If you expect your data to be highly numeric, then rows that contain 5% or greater of alphabetic characters will be removed.