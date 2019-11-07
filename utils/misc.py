import discord


def who_is(target: str, message: discord.Message) -> discord.User:
    """
        Identities if and who is being mentioned in the message, using explicit
        target string if no mentions were used.
        Returns empty string if none or multiple found.
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
