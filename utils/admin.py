from discord import User


# TODO: make dynamic
ADMINS = ["114643254451896328", "562784545242349568", "117770625635844102"]


def is_privileged(user: User, vips: list) -> bool:
    return str(user.id) in vips
