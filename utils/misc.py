"""Miscellaneous functions."""
import random

import discord
import xkcd
from typing import List

ROCK = "✊"
PAPER = "🖐️"
SCISSORS = "✌️"
LIZARD = "🤏"
SPOCK = "🖖"


def rock_paper_scissors() -> str:
    return random.choice([ROCK, PAPER, SCISSORS])


def rock_paper_scissors_lizard_spock() -> str:
    return random.choice([ROCK, PAPER, SCISSORS, LIZARD, SPOCK])


def rock_paper_scissors_lizard_spock_rules() -> str:
    return "https://shorturl.at/goAOS"


def who_is(target: str, message: discord.Message) -> str:
    """Identity who is being mentioned in the message.

    Arguments:
        target {str} -- Target name input.
        message {discord.Message} -- Original message, as context.

    Returns:
        Name of the user, or empty string if none found.

    """
    # The reason for separating target and message, even though target can be
    # obtained from message, is that different commands might have different ways
    # for extracting the target.
    if message.mentions:
        if len(message.mentions) == 1:
            return message.mentions[0].display_name
        else:
            return ""
    else:  # no obvious targets
        for member in message.channel.members:
            # we ignore the user's original nick since it's optional
            if target.strip().lower() == member.display_name.lower():
                return member.display_name
    return ""


def random_emote(message: discord.Message) -> str:
    """Return random emote from the server that the message was in."""
    return random.choice(message.guild.emojis)


def random_xkcd() -> str:
    """Return a random xkcd url."""
    latest = xkcd.getLatestComicNum()
    return f"https://xkcd.com/{random.randint(1, latest)}/"


def poll(message: discord.Message) -> List[str]:
    """React to the message with multiple choices."""
    try:
        choices = int(message.content.split(" ")[1])
    except ValueError:
        choices = 4
    reactions: List[str] = []
    for i in range(0, choices):
        reactions += [str(chr(127462 + i))]
    return reactions


def strip_quotes(input_str: str) -> str:
    """Remove quotes from string."""
    if input_str.startswith('"') and input_str.endswith('"'):
        input_str = input_str[1:-1]
    if input_str.startswith("'") and input_str.endswith("'"):
        input_str = input_str[1:-1]
    return input_str
