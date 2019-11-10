from unittest import TestCase

from ..utils.data import EasterEgg


class TestEasterEgg(TestCase):
    def setUp(self):
        self.eggs = [
            EasterEgg(*l) for l in [
                # key, operator, response, disabled, react
                ["a", "match", "re match", "", ""],
                ["b", "contains", "re contains", "", ""],
                ["c", "prefix", "re prefix", "", ""],
                ["d", "suffix", "re suffix", "", ""],
                ["e", "contains_word", "re contains word", "", ""],
                ["[fgh]", "regex", "re re", "", ""],
            ]
        ]
        self.match_egg = self.eggs[0]
        self.contains_egg = self.eggs[1]
        self.prefix_egg = self.eggs[2]
        self.suffix_egg = self.eggs[3]
        self.contains_word_egg = self.eggs[4]
        self.regex_egg = self.eggs[5]

    def test_match_egg(self):
        tests = [["a", True], ["I have a dog", False]]
        for testcase, answer in tests:
            with self.subTest():
                self.assertEqual(
                    answer, self.match_egg.trigger_on_str(testcase))

    def test_contains_egg(self):
        tests = [["b", True], ["I have b dog", True], ["I have bog", True]]
        for testcase, answer in tests:
            with self.subTest():
                self.assertEqual(
                    answer, self.contains_egg.trigger_on_str(testcase))

    def test_prefix_egg(self):
        tests = [["c", True], ["I have a cog", False], ["cog", True]]
        for testcase, answer in tests:
            with self.subTest():
                self.assertEqual(
                    answer, self.prefix_egg.trigger_on_str(testcase))

    def test_suffix_egg(self):
        tests = [["d", True], ["I have a dog", False], ["dod", True]]
        for testcase, answer in tests:
            with self.subTest():
                self.assertEqual(
                    answer, self.suffix_egg.trigger_on_str(testcase))

    def test_contains_word_egg(self):
        tests = [["e", True], ["I have e dog", True], ["I have deg", False]]
        for testcase, answer in tests:
            with self.subTest():
                self.assertEqual(
                    answer, self.contains_word_egg.trigger_on_str(testcase)
                )

    def test_regex_egg(self):
        tests = [["f", True], ["I have a dog", True], ["I have doh", True]]
        for testcase, answer in tests:
            with self.subTest():
                self.assertEqual(
                    answer, self.regex_egg.trigger_on_str(testcase))
