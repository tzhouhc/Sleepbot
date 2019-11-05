import random

# TODO:
# Centralize all Sibyl functions and global vars into a single Sibyl object
# that goes around and shoots stuff.


def is_separate_jurisdiction(target: str) -> bool:
    # can sibyl judge itself? Yes, yes she can.
    return target.strip().lower() in [
        "syraleaf!",
        "replayvalue",
        "tzhou",
    ]


def is_criminally_asymptotic(target: str) -> bool:
    return target.strip().lower() in [
        "tzhou",
        "syraleaf!",
        "replayvalue",
        # due to someone's misspelling
        "sibyl",
        "sybil",
    ]


def is_inherently_evil(target: str) -> bool:
    return target.strip().lower() in ["amadeus"]


def calculate_coefficient(target) -> int:
    if is_criminally_asymptotic(target):
        return 0
    elif is_inherently_evil(target):
        return random.randint(301, 500)
    else:
        # usually safe
        if random.randint(1, 5) <= 4:
            return random.randint(0, 100)
        else:
            return random.randint(101, 500)


# returns a number for lethality, and a string for announcement
def dominator_decision(target: str, coefficient: int) -> (int, str):
    if is_separate_jurisdiction(target):
        return 0, f"Target '{target}' is not under current jurisdiction."

    response = f"Target '{target}' has a crime coefficent of {coefficient}. "
    if coefficient == 0:
        response += "Target is literally a fucking saint."
        return 0, response
    elif coefficient < 100:
        response += "Not a target for enforcement action, the trigger will be locked."
        return 0, response
    elif coefficient < 300:
        response += (
            "They're a target for enforcement action. Enforcement Mode"
            " is Paralyzer. The safety will be released."
        )
        return 1, response
    elif coefficient == 500:
        response += (
            "They're a target for enforcement action. Enforcement Mode"
            " is Atomic Disassembler. Like, dude, how bad can you be?"
        )
        return 2, response
    else:
        response += (
            "They're a target for enforcement action. Enforcement Mode"
            "is Lethal Eliminator. Aim Carefully and Eliminate the Target."
        )
        return 2, response
