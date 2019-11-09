#!/usr/bin/env python3
import argparse
from typing import Optional

import discord

from utils.admin import ADMINS, is_privileged
from utils.data import EasterHen, get_config_from_json_file
from utils.misc import random_emote, who_is
from utils.response import ResponseManager
from utils.sibyl import SibylSystem


class SleepbotClient(discord.Client):
    def __init__(self) -> None:
        super().__init__()
        self.sibyl: Optional[SibylSystem] = None
        self.response_manager: Optional[ResponseManager] = None

    def set_response_manager(self, rm: ResponseManager) -> None:
        self.response_manager = rm

    def set_sibyl(self, sibyl: SibylSystem) -> None:
        self.sibyl = sibyl

    async def on_ready(self) -> None:
        print(f"We have logged in as {self.user}")

    async def on_message(self, message: discord.Message) -> None:
        assert self.sibyl is not None
        assert self.response_manager is not None
        # skip own messages
        if message.author == self.user:
            return

        # ===============
        # toy methods
        # ===============
        elif message.content.strip().lower().startswith("vibe check"):
            await message.channel.send(random_emote(message))

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

        # generic easter egg response system
        elif message.content == "!refresh":
            self.response_manager.refresh()
        else:
            egg = self.response_manager.get_triggered_eggs(
                message.content.strip().lower()
            )
            if egg:
                if egg.react:
                    for emote in egg.response.split("/"):
                        await message.add_reaction(emote)
                else:
                    await message.channel.send(egg.response)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Start the sleep monitor bot.")
    parser.add_argument(
        "-c",
        "--config-json",
        type=argparse.FileType("r"),
        help="The json-file containing the token for the bot. It needs to be "
        "an object with the fields 'token' and 'easter_hen_url'.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config_data = get_config_from_json_file(args.config_json)
    client = SleepbotClient()
    response_manager = ResponseManager()
    response_manager.set_hen(EasterHen(config_data.get("easter_hen_url")))
    client.set_sibyl(SibylSystem())
    client.set_response_manager(response_manager)
    client.run(config_data.get("token"))


if __name__ == "__main__":
    main()
