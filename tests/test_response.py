import unittest

from ..utils import response


class TestResponse(unittest.TestCase):
    def setUp(self):
        self.rm = response.ResponseManager()

    def test_operate_on_strings(self):
        inputs = [
            [["match", "12", "12"], True],
            [["match", "13", "12"], False],
            [["match", "13", "1132"], False],
            [["prefix", "13", "1132"], False],
            [["prefix", "13", "1332"], True],
            [["prefix", "13", "332"], False],
            [["suffix", "13", "1132"], False],
            [["suffix", "13", "13"], True],
            [["suffix", "13", "113"], True],
            [["contains", "13", "1132"], True],
            [["contains", "13", "11032"], False],
            [["contains_word", "13", "1132"], False],
            [["contains_word", "13", "1 132"], False],
            [["contains_word", "13", "1 13 2"], True],
            [["contains_word", "13", "1 13, 2"], True],
            [["regex", "1{2,}3", "1 132"], False],
            [["regex", "1{2,}3", "11132"], True],
            [["regex", "1{2,}3", "1132"], True],
        ]
        for args, answer in inputs:
            with self.subTest():
                self.assertEqual(answer, self.rm.should_operate_on_strings(*args))
