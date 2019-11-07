import csv
import json
from io import StringIO
from typing import List

import requests


def get_config_from_json_file(fileio: StringIO):
    return json.load(fileio)


class EasterEgg(object):
    def __init__(self, easter_line):
        keyword, operator, response, disabled, react, func_response = easter_line
        self.keyword = keyword.strip().lower()
        self.operator = operator.strip().lower()
        self.response = response
        self.disabled = disabled.strip().lower() == "true"
        self.react = react.strip().lower() == "true"
        self.func_response = func_response.strip().lower() == "true"


class EasterHen(object):
    def __init__(self, source_url: str) -> None:
        self.source = source_url
        self.eggs: List[EasterEgg] = []
        self.refresh()

    def refresh(self) -> None:
        res = requests.get(url=self.source)
        reader = csv.reader(
            StringIO(res.content.decode("utf-8")), delimiter=",", quotechar='"'
        )
        next(reader)  # skip header
        for egg in map(EasterEgg, reader):
            self.eggs += [] if (egg.disabled or not egg.response) else [egg]

    def get_eggs(self) -> List[EasterEgg]:
        return self.eggs
