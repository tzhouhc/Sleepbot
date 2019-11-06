import unittest

from ..utils import response


class TestResponse(unittest.TestCase):
    def test_operate_on_strings(self):
        inputs = [
            [["match", "12", "12"], True],
        ]
        for args, answer in inputs:
            self.assertEqual(answer, response.operate_on_strings(*args))
