# -*- coding: utf-8 -*-
"""
Created on 2024-10-22

author: jvorsten
"""

# Python imports
import unittest
from typing import List

# Third party imports

# Local imports
from scripts.data_cleaning_utilities import _fill_empty_line_with_previous_data


# %%

class Test_data_cleaning_utilities(unittest.TestCase):

    def test__fill_empty_line_with_previous_data(self):
        """Test function _fill_empty_line_with_previous_data"""
        # First, create a list of data with all strings in the list filled
        test_list_1: List[str] = ['a', 'b', 'c', 'd', 'e']
        previous_list: List[str] = ['1', '2', '3', '4', '5']
        _fill_empty_line_with_previous_data(test_list_1, previous_list)
        # No strings in the list should be modified
        self.assertEqual(test_list_1[0], 'a')
        self.assertEqual(test_list_1[1], 'b')
        self.assertEqual(test_list_1[2], 'c')
        self.assertEqual(test_list_1[3], 'd')
        self.assertEqual(test_list_1[4], 'e')


        # Now, creat a list of strings with some empty strings
        test_list_2: List[str] = ['a', '', 'c', 'd', 'e']
        _fill_empty_line_with_previous_data(test_list_2, previous_list)
        self.assertEqual(test_list_2[0], 'a')
        self.assertEqual(test_list_2[1], '2')
        self.assertEqual(test_list_2[2], 'c')
        self.assertEqual(test_list_2[3], 'd')
        self.assertEqual(test_list_2[4], 'e')

        # Continue to test cases
        test_list_3: List[str] = ['', 'b', 'c', 'd', 'e']
        _fill_empty_line_with_previous_data(test_list_3, previous_list)
        self.assertEqual(test_list_3[0], '1')
        self.assertEqual(test_list_3[1], 'b')
        self.assertEqual(test_list_3[2], 'c')
        self.assertEqual(test_list_3[3], 'd')
        self.assertEqual(test_list_3[4], 'e')

        # Continue to test cases
        test_list_4: List[str] = ['a', 'b', 'c', 'd', '']
        _fill_empty_line_with_previous_data(test_list_4, previous_list)
        self.assertEqual(test_list_4[0], 'a')
        self.assertEqual(test_list_4[1], 'b')
        self.assertEqual(test_list_4[2], 'c')
        self.assertEqual(test_list_4[3], 'd')
        self.assertEqual(test_list_4[4], '5')
        
        # This is probably not needed but the previous_list should not be mutable
        self.assertEqual(previous_list[0], '1')
        self.assertEqual(previous_list[1], '2')
        self.assertEqual(previous_list[2], '3')
        self.assertEqual(previous_list[3], '4')
        self.assertEqual(previous_list[4], '5')

        return None

if __name__ == '__main__':
    unittest.main()