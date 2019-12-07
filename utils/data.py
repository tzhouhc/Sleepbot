"""Module for handling Sleepbot external data sources."""
import csv
import json
import re

from datetime import datetime
from io import StringIO
from typing import Callable, List, Optional, Dict

import requests

DEFAULT_DELAY = 0


def get_config_from_json_file(fileio: StringIO) -> Dict[str, str]:
    """Obtain Sleepbot configs from json.

    Arguments:
        fileio {StringIO} -- IO object containing json formatted data.

    Returns:
        Dict -- Config data as a dict.

    """
    return json.load(fileio)


class EasterEgg(object):
    """Class for easter eggs."""

    def __init__(
        self,
        keyword: str,
        operator: str,
        response: str,
        disabled="",
        react="",
        delay="",
    ) -> None:
        """Create an easter egg.

        Arguments:
            keyword {str} -- The string that triggers the easter egg
            operator {str} -- The criteria to match against, e.g. 'contains'
            response {str} -- The response to give in case of a trigger.

        Keyword Arguments:
            disabled {str} -- Whether the egg is disabled. (default: {""})
            react {str} -- Whether the resposne should be a reaction. (default: {""})
            delay {str} -- Whether to rate-limit the egg. (default: {""})
        """
        self.keyword = keyword.strip().lower()
        # compile_operator needs to be after self.keyword initialization
        self.operator = self.compile_operator(operator.strip().lower())
        self.response = response
        self.disabled = disabled.strip().lower() == "true"
        self.react = react.strip().lower() == "true"
        self.delay = int(delay) if delay else DEFAULT_DELAY
        self.last_triggered: Optional[datetime] = None

    def compile_operator(self, operator: str) -> Callable[[str], bool]:
        """Convert an operator string to a function.

        The function can be latter called to check whether they trigger the egg.
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

    def is_in_timeout(self) -> bool:
        """Whether the egg is in 'cooldown' and cannot be triggered for now."""
        return (
            self.last_triggered is not None
            and (datetime.now() - self.last_triggered).seconds < self.delay
        )

    def trigger_on_str(self, input: str) -> bool:
        """Whether the egg should trigger on the input.

        Arguments:
            input {str} -- The text to attempt to match the egg against.
        """
        if self.operator(input):
            if not self.is_in_timeout():
                self.last_triggered = datetime.now()
                return True
        return False


class EasterHen(object):
    """Class for source of easter eggs."""

    def __init__(self, source_url: str) -> None:
        """Create a source for easter eggs using online csv files.

        Arguments:
            source_url {str} -- Where to obtain list of egg source data.
        """
        self.source = source_url
        self.eggs: List[EasterEgg] = []
        self.refresh()

    def refresh(self) -> None:
        """Refetches from the data source."""
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
        """Return the list of eggs.

        Returns:
            List[EasterEgg] -- List of EasterEgg objects.

        """
        return self.eggs
