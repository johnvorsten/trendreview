# encoding UTF-8
"""
Created 2022-5-26

Remove bad lines from a .csv file based on a set of rules
1. If a line contains no data, then remove the line
2. This data is primarily numeric. If the data is primarily (greater than 5%) 
word characters then remove the line

author John Vorsten
"""

# Python imports
import unittest
from typing import List

# Third party imports

# Local imports
from clean_csv import _is_line_empty, _is_line_primarily_numeric

# Declarations

#%% 

class TestCleanCSV(unittest.TestCase):
    """Test cleaning script"""

    def test__is_line_empty(self):
        """All commas should be empty lines"""

        self.assertTrue(_is_line_empty(['','','','','','',]))
        self.assertFalse(_is_line_empty(['','','','','a',]))

        return False

    def test__is_line_primarily_numeric(self):
        """Greater than 5% of alphabetic characters should return False"""
        line1: List[str] = ['1','2','3','4','5','6','7','8','9','10'] # True
        line2: List[str] = ['1','2','3','4','5','6','7','8','9','a'] # False
        line3: List[str] = []
        for _ in range(0,96):
            line3.append(str(float(1.02)))
        for _ in range(0, 4):
            line3.append(str('a'))

        self.assertTrue(_is_line_primarily_numeric(line1))
        self.assertFalse(_is_line_primarily_numeric(line2))
        self.assertTrue(_is_line_primarily_numeric(line3))

if __name__ == '__main__':
    unittest.main()