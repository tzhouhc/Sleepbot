import argparse

from typing import List
from discord import User


def simple_parser() -> argparse.ArgumentParser:
    """A simple parser that takes a single amorphous string argument."""
    parser = argparse.ArgumentParser()
    parser.add_argument("INPUT", "Generic one-param input", type=str)
    return parser


def person_parser(userlist: List[User]) -> argparse.ArgumentParser:
    """A simple parser that takes a single username for argument."""

    def find_person_from_list(input: str) -> str:
        for member in userlist:
            # we ignore the user's original nick since it's optional
            if input.strip().lower() == member.display_name.lower():
                return member.display_name
        return ""

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "PERSON", "Input parser for a person", type=find_person_from_list
    )
    return parser
