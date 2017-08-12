import unittest
from party_name_extraction import get_party_names

test_case = 'the name is between Sksm Inc. and Asmdav Asda Inc.'
class test_party_names(unittest.TestCase):

    def test_first_name(self):
        self.assertEqual(get_party_names(test_case), ['between Sksm Inc.', 'and Asmdav Asda Inc.'])

if __name__ == '__main__':
    unittest.main()
