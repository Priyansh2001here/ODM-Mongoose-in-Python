import unittest
from typing import List
from odm import Validator

v = Validator()


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
        x = v.validate(odm, data)
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
        x = v.validate(odm, data)
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

        x = v.validate(odm, data_true)
        self.assertTrue(x)
        x = v.validate(odm, data_false)
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

        x = v.validate(odm, data_true)
        self.assertTrue(x)
        x = v.validate(odm, data_false)
        self.assertFalse(x)
        x = v.validate(odm, data_false_2)
        self.assertFalse(x)

    def test_list_of_list(self):
        odm = {
            'data': List[List[int]]
        }

        data = {
            'data': [[1, 3, 4]]
        }

        x = v.validate(odm, data)
        self.assertTrue(x)

        data = {
            'data': [['Priyansh']]
        }
        x = v.validate(odm, data)
        self.assertFalse(x)

        data = {
            'data': [9, 5, 6]
        }
        x = v.validate(odm, data)
        self.assertFalse(x)

    def test_new(self):
        odm = {
            'data': List[List[int]]
        }
        data = {
            'data': {}
        }

        x = v.validate(odm, data)
        self.assertFalse(x)

        data = {
            'data': []
        }

        x = v.validate(odm, data)
        self.assertTrue(x)


class Dictionary(unittest.TestCase):

    def test_1D(self):
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

        is_valid = v.validate(odm, data)
        self.assertTrue(is_valid)

        data = {
            'name': {
                'first name': 'Priyansh',
                'last name': 'Singh'
            },
            'number of frnds': '3'
        }

        is_valid = v.validate(odm, data)
        self.assertFalse(is_valid)

        data = {
            'name': {
                'first name': 'Priyansh',
                'last name': 89763
            },
            'number of frnds': 3
        }

        is_valid = v.validate(odm, data)
        self.assertFalse(is_valid)

    def test_2D(self):
        odm = {
            'add': {
                'coordinates': {
                    'lat': int,
                    'long': int
                }
            }
        }

        data = {
            'add': {
                'coordinates': {
                    'lat': 19,
                    'long': 12
                }
            }
        }

        x = v.validate(odm, data)
        self.assertTrue(x)

        data = {
            'add': {
                'coordinates': {
                    'lat': 'Priyansh',
                    'long': 12
                }
            }
        }

        x = v.validate(odm, data)
        self.assertFalse(x)

        data = {
            'add': {
                'coordinates': {
                    'lat': 19,
                    'long': 'Singh'
                }
            }
        }

        x = v.validate(odm, data)
        self.assertFalse(x)

        odm = {
            'add': {
                'coordinates': {
                    'lat': List[int],
                    'long': int
                }
            }
        }

        data = {
            'add': {
                'coordinates': {
                    'lat': 19,
                    'long': 12
                }
            }
        }

        x = v.validate(odm, data)
        self.assertFalse(x)

        data = {
            'add': {
                'coordinates': {
                    'lat': [12, 23, 5],
                    'long': 12
                }
            }
        }

        x = v.validate(odm, data)
        self.assertTrue(x)

        data = {
            'add': {
                'coordinates': {
                    'lat': [[19]],
                    'long': 12
                }
            }
        }

        x = v.validate(odm, data)
        self.assertFalse(x)


if __name__ == '__main__':
    unittest.main()
