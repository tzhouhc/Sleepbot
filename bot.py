#!/usr/bin/env python3
import argparse
import cachetools
import discord

from utils.data import get_config_from_json_file, EasterHen
from utils.sibyl import calculate_coefficient, dominator_decision
from utils.response import operate_on_strings
from utils.misc import who_is


# declare empty hen and populate later
EASTER_HEN = None
SIBYL_CACHE = cachetools.TTLCache(64, ttl=100)
DOMINATOR_STATUS = 0
DOMINATOR_LAST_TARGET = None


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
    global DOMINATOR_STATUS
    global DOMINATOR_LAST_TARGET
    if target in SIBYL_CACHE:
        coefficient = SIBYL_CACHE.get(target)
    else:
        coefficient = calculate_coefficient(target)
        SIBYL_CACHE[target] = coefficient
    lethality, response = dominator_decision(target, coefficient)
    DOMINATOR_STATUS = lethality
    DOMINATOR_LAST_TARGET = target
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
    global DOMINATOR_LAST_TARGET
    global DOMINATOR_STATUS
    if message.author == client.user:
        return
    # TODO: add other toy methods
    elif message.content.startswith(".Dominator "):
        target = " ".join(message.content.split(" ")[1:])
        target_user = who_is(target, message)
        if not target_user:
            await message.channel.send(
                "Zero or multiple targets identified. Please select a single target."
            )
            return
        await message.channel.send(dominator(target_user))
    elif message.content.startswith(".DominatorFire"):
        if not DOMINATOR_LAST_TARGET or DOMINATOR_STATUS == 0:
            await message.channel.send("Dominator is locked.")
        elif DOMINATOR_STATUS == 1:
            await message.channel.send(
                f"> {DOMINATOR_LAST_TARGET} <: https://gfycat.com/scarcejoyousfinwhale"
            )
            del SIBYL_CACHE[DOMINATOR_LAST_TARGET]
        else:
            await message.channel.send(
                f"> {DOMINATOR_LAST_TARGET}< : https://gfycat.com/regulartarthorseshoecrab"
            )
            del SIBYL_CACHE[DOMINATOR_LAST_TARGET]
        DOMINATOR_LAST_TARGET = None
        DOMINATOR_STATUS = 0

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
