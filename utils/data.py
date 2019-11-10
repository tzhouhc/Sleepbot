import csv
import json
import re
from io import StringIO
from typing import Callable, List

import requests


def get_config_from_json_file(fileio: StringIO):
    return json.load(fileio)


class EasterEgg(object):
    def __init__(
        self, keyword: str, operator: str, response: str, disabled="", react=""
    ):
        self.keyword = keyword.strip().lower()
        # compile_operator needs to be after self.keyword initialization
        self.operator = self.compile_operator(operator.strip().lower())
        self.response = response
        self.disabled = disabled.strip().lower() == "true"
        self.react = react.strip().lower() == "true"

    def compile_operator(self, operator: str) -> Callable[[str], bool]:
        """
            Converts an operator string to a function that can be latter called
            to check whether they trigger the egg.
        """
        if operator == "match":
            return lambda x: self.keyword == x
        elif operator == "contains_word":
            pattern = re.compile(fr"\b{self.keyword}\b")
            return lambda x: pattern.search(x) is not None
        elif operator == "prefix":
            return lambda x: x.startswith(self.keyword)
        elif operator == "suffix":
            return lambda x: x.endswith(self.keyword)
        elif operator == "contains":
            return lambda x: self.keyword in x
        elif operator == "regex":
            pattern = re.compile(fr"{self.keyword}")
            return lambda x: pattern.search(x) is not None
        else:
            print(f"operator '{operator}' not recognized.")
            return lambda x: False

    def trigger_on_str(self, input: str) -> bool:
        return self.operator(input)


class EasterHen(object):
    def __init__(self, source_url: str) -> None:
        self.source = source_url
        self.eggs: List[EasterEgg] = []
        self.refresh()

    def refresh(self) -> None:
        self.eggs = []
        res = requests.get(url=self.source)
        reader = csv.reader(
            StringIO(res.content.decode("utf-8")), delimiter=",", quotechar='"'
        )
        next(reader)  # skip header
        for line in reader:
            egg = EasterEgg(*line)
            self.eggs += [] if (egg.disabled or not egg.response) else [egg]

    def get_eggs(self) -> List[EasterEgg]:
        return self.eggs
