import unittest
from abc_classes import *


class TestABCClasses(unittest.TestCase):
    def setUp(self):
        self.case_data = [231, 34.343, -0.23, -131, 0.3, 434.2, 232]
        self.case_res = [23321, 234.243, 20.3]
        self.a = A(self.case_data, self.case_res)

    def test_init(self):
        self.assertEqual(self.a.data, self.case_data)
        self.assertEqual(self.a.result, self.case_res)

    def test_get_answer(self):
        case = [1, 1, 0, 0, 0, 1, 1]
        self.assertEqual(self.a.get_answer(), case)

    def tearDown(self):
        del self.a


if __name__ == "__main__":
    unittest.main()
