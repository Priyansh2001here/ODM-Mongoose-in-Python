import unittest
from odm import check
from typing import List


class OneDimensional(unittest.TestCase):

    def test_true(self):
        data = {
            'name': 'priyansh singh',
            'age': 19,
            'address': '113 north city pilibhit road'
        }

        odm = {
            'name': str,
            'age': int,
            'address': str
        }
        x = check(odm, data)
        self.assertTrue(x)

    def test_false(self):
        data = {
            'name': 'priyansh singh',
            'age': 19,
            'address': '113 north city pilibhit road'
        }

        odm = {
            'name': str,
            'age': int,
            'address': int
        }
        x = check(odm, data)
        self.assertFalse(x)


class DictionaryOfList(unittest.TestCase):

    def test_true_list_of_strings(self):
        data_true = {
            'name': 'priyansh singh',
            'age': 19,
            'address': '113 north city pilibhit road',
            'friends': [
                'Priyansh Singh',
                'Shivank Mittal',
                'Naman Agarwal',
                'Himalaya Gupta'
            ]
        }

        data_false = {
            'name': 'priyansh singh',
            'age': 19,
            'address': '113 north city pilibhit road',
            'friends': [
                19,
                20,
                30
            ]
        }

        odm = {
            'name': str,
            'age': int,
            'address': str,
            'friends': List[str]
        }

        x = check(odm, data_true)
        self.assertTrue(x)
        x = check(odm, data_false)
        self.assertFalse(x)

    def test_list_of_integers(self):
        data_true = {
            'numbers': [1, 2, 3, 4, 4, 1, 9, 5]
        }

        data_false = {
            'numbers': ['Priyansh Singh']
        }

        data_false_2 = {
            'numbers': 3
        }

        odm = {
            'numbers': List[int]
        }

        x = check(odm, data_true)
        self.assertTrue(x)
        x = check(odm, data_false)
        self.assertFalse(x)
        x = check(odm, data_false_2)
        self.assertFalse(x)

    def test_list_of_list(self):
        odm = {
            'data': List[List[int]]
        }

        data = {
            'data': [[1, 3, 4]]
        }

        x = check(odm, data)
        self.assertTrue(x)

        data = {
            'data': [['Priyansh']]
        }
        x = check(odm, data)
        self.assertFalse(x)

        data = {
            'data': [9, 5, 6]
        }
        x = check(odm, data)
        self.assertFalse(x)

    def test_new(self):
        odm = {
            'data': List[List[int]]
        }
        data = {
            'data': {}
        }

        x = check(odm, data)
        self.assertFalse(x)

        data = {
            'data': []
        }

        x = check(odm, data)
        self.assertTrue(x)

################# todo #####################
class Dictionary(unittest.TestCase):

    def test_dict(self):
        odm = {
            'name': {
                'first name': str,
                'last name': str
            },
            'number of frnds': int
        }

        data = {
            'name': {
                'first name': 'Priyansh',
                'last name': 'Singh'
            },
            'number of frnds': 3
        }

        is_valid = check(odm, data)
        self.assertTrue(is_valid)

        data = {
            'name': {
                'first name': 'Priyansh',
                'last name': 'Singh'
            },
            'number of frnds': '3'
        }

        is_valid = check(odm, data)
        self.assertFalse(is_valid)

        data = {
            'name': {
                'first name': 'Priyansh',
                'last name': 89763
            },
            'number of frnds': 3
        }

        is_valid = check(odm, data)
        self.assertFalse(is_valid)


if __name__ == '__main__':
    unittest.main()
