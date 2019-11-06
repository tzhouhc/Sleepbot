#!/usr/bin/env python3
import argparse
import discord

from utils.data import get_config_from_json_file, EasterHen
from utils.sibyl import SibylSystem  # calculate_coefficient, dominator_decision
from utils.response import operate_on_strings
from utils.misc import who_is
from utils.admin import ADMINS, is_privileged


class SleepbotClient(discord.Client):
    def __init__(self) -> None:
        super().__init__()
        self.easter_hen = None
        self.sibyl = None

    def set_easter_hen(self, hen: EasterHen) -> None:
        self.easter_hen = hen

    def set_sibyl(self, sibyl: SibylSystem) -> None:
        self.sibyl = sibyl

    async def on_ready(self) -> None:
        print(f"We have logged in as {self.user}")

    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user:
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
            await message.channel.send(self.sibyl.dominator_decision(target_user))
        # AHEM
        elif message.content.startswith(".DominatorSet"):
            # cancel in case of pleb abuse
            if not is_privileged(message.author, ADMINS):
                return
            target = " ".join(message.content.split(" ")[1:-1])
            value = message.content.split(" ")[-1]
            target_user = who_is(target, message)
            self.sibyl.dominator_force(target_user, int(value))
        elif message.content.startswith(".DominatorFire"):
            await message.channel.send(self.sibyl.dominator_fire())
        elif message.content == "!refresh":
            self.easter_hen.refresh()
        else:
            react, response = base_response(
                message.content.strip().lower(), hen=self.easter_hen
            )
            if response:
                if react:
                    for emote in response.split("/"):
                        await message.add_reaction(emote)
                else:
                    await message.channel.send(response)


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


def main() -> None:
    args = parse_args()
    config_data = get_config_from_json_file(args.config_json)
    client = SleepbotClient()
    client.set_easter_hen(EasterHen(config_data.get("easter_hen_url")))
    client.set_sibyl(SibylSystem())
    client.run(config_data.get("token"))


if __name__ == "__main__":
    main()
