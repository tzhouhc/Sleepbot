"""Miscellaneous functions."""
import random

import discord
import xkcd


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
