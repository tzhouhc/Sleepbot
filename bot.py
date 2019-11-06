#!/usr/bin/env python3
import argparse
import discord

from utils.data import get_config_from_json_file, EasterHen
from utils.sibyl import SibylSystem  # calculate_coefficient, dominator_decision
from utils.response import operate_on_strings
from utils.misc import who_is
from utils.admin import ADMINS, is_privileged


# declare empty hen and populate later
EASTER_HEN = None
SIBYL = None
# SIBYL_CACHE = cachetools.TTLCache(64, ttl=100)
# DOMINATOR_STATUS = 0
# DOMINATOR_LAST_TARGET = None


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
    global SIBYL
    # if target in SIBYL_CACHE:
    # coefficient = SIBYL_CACHE.get(target)
    # else:
    # coefficient = calculate_coefficient(target)
    # SIBYL_CACHE[target] = coefficient
    response = SIBYL.dominator_decision(target)
    return response


# Top level function to handle the base case of messages
# Tries to find *some* keyword in the message to respond to according to the
# easter-egg table
def base_response(message_text: str, hen: EasterHen) -> list:
    for keyword, operator, response, disabled, react in hen.get_eggs():
        keyword = keyword.strip().lower()
        operator = operator.strip().lower()
        disabled = disabled.strip().lower()
        reaction = react.strip().lower() == "true"
        if disabled == "true" or not response:
            continue
        if operate_on_strings(operator, keyword, message_text):
            return reaction, response
    return False, ""


@client.event
async def on_ready() -> None:
    print(f"We have logged in as {client.user}")


@client.event
async def on_message(message: discord.Message) -> None:
    global EASTER_HEN
    global SIBYL
    if message.author == client.user:
        return
    # TODO: add other toy methods
    elif message.content.startswith(".Dominator "):
        # TODO: use argparse for command options
        target = " ".join(message.content.split(" ")[1:])
        target_user = who_is(target, message)
        if not target_user:
            await message.channel.send(
                "Zero or multiple targets identified. Please select a single target."
            )
            return
        await message.channel.send(SIBYL.dominator_decision(target_user))
    # AHEM
    elif message.content.startswith(".DominatorSet"):
        # cancel in case of pleb abuse
        if not is_privileged(message.author, ADMINS):
            return
        target = " ".join(message.content.split(" ")[1:-1])
        value = message.content.split(" ")[-1]
        target_user = who_is(target, message)
        SIBYL.dominator_force(target_user, int(value))
    elif message.content.startswith(".DominatorFire"):
        await message.channel.send(SIBYL.dominator_fire())
    elif message.content == "!refresh":
        EASTER_HEN.refresh()
    else:
        react, response = base_response(message.content.strip().lower(), hen=EASTER_HEN)
        if response:
            if react:
                for emote in response.split("/"):
                    await message.add_reaction(emote)
            else:
                await message.channel.send(response)


def main() -> None:
    global EASTER_HEN
    global SIBYL
    args = parse_args()
    config_data = get_config_from_json_file(args.config_json)
    EASTER_HEN = EasterHen(config_data.get("easter_hen_url"))
    SIBYL = SibylSystem()
    client.run(config_data.get("token"))


if __name__ == "__main__":
    main()
