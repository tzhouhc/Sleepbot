#!/usr/bin/env python3
import argparse
import cachetools
import discord
import random

from utils.data import get_config_from_json_file, EasterHen
from utils.sibyl import is_criminally_asymptotic
from utils.response import operate_on_strings


# declare empty hen and populate later
EASTER_HEN = None
SIBYL_CACHE = cachetools.TTLCache(64, ttl=100)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Start the sleep monitor bot.")
    parser.add_argument(
        "-c",
        "--config-json",
        type=argparse.FileType("r"),
        help="The json-file containing the token for the bot. It needs to be "
        "an object with the fields 'token' and 'easter_hen_url'.",
    )
    return parser.parse_args()


client = discord.Client()


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


# Top level function to handle the base case of messages
# Tries to find *some* keyword in the message to respond to according to the
# easter-egg table
def base_response(message_text: str, hen: EasterHen) -> str:
    for keyword, operator, response, disabled in hen.get_eggs():
        keyword = keyword.strip().lower()
        operator = operator.strip().lower()
        disabled = disabled.strip().lower()
        if disabled == "true" or not response:
            continue
        if operate_on_strings(operator, keyword, message_text):
            return response
    return ""


@client.event
async def on_ready() -> None:
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message: discord.Message) -> None:
    global EASTER_HEN
    if message.author == client.user:
        return
    # TODO: add other toy methods
    elif message.content.startswith(".Dominator "):
        target = " ".join(message.content.split(" ")[1:])
        await message.channel.send(dominator(target))
    elif message.content == "!refresh":
        EASTER_HEN.refresh()
    else:
        response = base_response(message.content.strip().lower(), hen=EASTER_HEN)
        if response:
            await message.channel.send(response)


def main() -> None:
    global EASTER_HEN
    args = parse_args()
    config_data = get_config_from_json_file(args.config_json)
    EASTER_HEN = EasterHen(config_data.get("easter_hen_url"))
    client.run(config_data.get("token"))


if __name__ == "__main__":
    main()
