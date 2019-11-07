import unittest

from ..utils.sibyl import SibylSystem


class TestSibyl(unittest.TestCase):
    def setUp(self):
        self.sibyl = SibylSystem()
