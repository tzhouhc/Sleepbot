#!/usr/bin/env python3
import argparse
import csv
import discord
import requests
from io import StringIO

# TODO: full PEP484 compliance

# TODO: make this also a parameter to read from a local config file or pass in
# on the command line
REPLAY_VALUE_EASTER_HEN_URL = "https://docs.google.com/spreadsheets/d/1cCUBJNXRoCaOh6uE4pDYW9mZ_6sFtSG0E2YJZCGwvPQ/export?format=csv"
EASTER_HEN = []


def parse_args():
    parser = argparse.ArgumentParser(description="Start the sleep monitor bot.")
    token_parser_group = parser.add_mutually_exclusive_group(required=True)

    token_parser_group.add_argument("--token", type=str, help="The token for the bot.")
    token_parser_group.add_argument(
        "--token-file",
        type=argparse.FileType("r"),
        help="The file containing the token for the bot.",
    )
    return parser.parse_args()


client = discord.Client()


def operate_on_strings(operator: str, sub_operand: str, operand: str) -> bool:
    if operator == "MATCH":
        return sub_operand == operand
    elif operator == "PREFIX":
        return operand.startswith(sub_operand)
    elif operator == "SUFFIX":
        return operand.endswith(sub_operand)
    elif operator == "CONTAINS":
        return sub_operand in operand
    else:  # operator not recognized
        # TODO: do actual logging instead of stdout print
        print(f"operator '{operator}' not recognized.")
        return False


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    global EASTER_HEN
    if message.author == client.user:
        return
    # TODO: add other toy methods
    elif message.content == "!refresh":
        EASTER_HEN = get_rules_from_google_sheet(REPLAY_VALUE_EASTER_HEN_URL)
    else:
        # currently ignore 'ignore_quotation'
        for keyword, operator, response, disabled in EASTER_HEN:
            if disabled.strip() == "TRUE" or not response:
                continue
            if operate_on_strings(
                operator, keyword.strip().lower(), message.content.strip().lower()
            ):
                await message.channel.send(response)


def get_rules_from_google_sheet(url) -> list:
    res = requests.get(url=url)
    reader = csv.reader(StringIO(res.text), delimiter=",", quotechar='"')
    next(reader)  # skip header
    return list(reader)


def get_token_from_file(fileio):
    return fileio.read().rstrip()


def main():
    args = parse_args()
    if not args.token:
        args.token = get_token_from_file(args.token_file)
    client.run(args.token)


if __name__ == "__main__":
    main()
