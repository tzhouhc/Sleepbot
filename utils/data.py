import csv
import json
import requests

from io import StringIO


def get_config_from_json_file(fileio: StringIO):
    return json.load(fileio)


class EasterHen(object):
    def __init__(self, source_url: str) -> None:
        self.source = source_url
        self.eggs = []
        self.refresh()

    def refresh(self) -> None:
        res = requests.get(url=self.source)
        reader = csv.reader(
            StringIO(res.content.decode("utf-8")), delimiter=",", quotechar='"'
        )
        next(reader)  # skip header
        self.eggs = list(reader)

    def get_eggs(self) -> list:
        return self.eggs
