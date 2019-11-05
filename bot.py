#!/usr/bin/env python3
import argparse
import cachetools
import csv
import discord
import random
import requests
from io import StringIO

# TODO: full PEP484 compliance


def get_rules_from_google_sheet(url) -> list:
    res = requests.get(url=url)
    reader = csv.reader(StringIO(res.text), delimiter=",", quotechar='"')
    next(reader)  # skip header
    return list(reader)


# TODO: make this also a parameter to read from a local config file or pass in
# on the command line
REPLAY_VALUE_EASTER_HEN_URL = "https://docs.google.com/spreadsheets/d/1cCUBJNXRoCaOh6uE4pDYW9mZ_6sFtSG0E2YJZCGwvPQ/export?format=csv"
EASTER_HEN = get_rules_from_google_sheet(REPLAY_VALUE_EASTER_HEN_URL)
SIBYL_CACHE = cachetools.TTLCache(64, ttl=100)


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
    if operator == "match":
        return sub_operand == operand
    elif operator == "prefix":
        return operand.startswith(sub_operand)
    elif operator == "suffix":
        return operand.endswith(sub_operand)
    elif operator == "contains":
        return sub_operand in operand
    else:  # operator not recognized
        # TODO: do actual logging instead of stdout print
        print(f"operator '{operator}' not recognized.")
        return False


def is_criminally_asymptotic(target: str) -> bool:
    return target.strip().lower() in [
        "tzhou",
        "syra",
        "syraleaf",
        "replay",
        "replayvalue",
        "replay value",
        "tz",
        "rep",
        "marv",
        "marvin",
    ]


def dominator(target: str) -> str:
    global SIBYL_CACHE
    if target in SIBYL_CACHE:
        coefficient = SIBYL_CACHE.get(target)
    else:
        coefficient = 0 if is_criminally_asymptotic(target) else random.randint(0, 499)
        SIBYL_CACHE[target] = coefficient
    response = f"Target has a crime coefficent of {coefficient}. "
    if coefficient == 0:
        response += "Target is literally a fucking saint."
    elif coefficient < 100:
        response += "Not a target for enforcement action, the trigger will be "
        "locked."
    elif coefficient < 300:
        response += "They're a target for enforcement action. Enforcement Mode"
        " is Paralyzer. The safety will be released."
    else:
        response += "They're a target for enforcement action. Enforcement Mode"
        "is Lethal Eliminator. Aim Carefully and Eliminate the Target."
    return response


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message):
    global EASTER_HEN
    if message.author == client.user:
        return
    # TODO: add other toy methods
    elif message.content.startswith(".Dominator"):
        target = " ".join(message.content.split(" ")[1:])
        await message.channel.send(dominator(target))
    elif message.content == "!refresh":
        EASTER_HEN = get_rules_from_google_sheet(REPLAY_VALUE_EASTER_HEN_URL)
    else:
        # currently ignore 'ignore_quotation'
        for keyword, operator, response, disabled in EASTER_HEN:
            keyword = keyword.strip().lower()
            operator = operator.strip().lower()
            disabled = disabled.strip().lower()
            if disabled == "true" or not response:
                continue
            if operate_on_strings(operator, keyword, message.content.strip().lower()):
                await message.channel.send(response)


def get_token_from_file(fileio):
    return fileio.read().rstrip()


def main():
    args = parse_args()
    if not args.token:
        args.token = get_token_from_file(args.token_file)
    client.run(args.token)


if __name__ == "__main__":
    main()
