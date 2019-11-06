import random
import enum
from cachetools import TTLCache


# Represents the states that the dominator can be in
class DominatorStatus(enum.Enum):
    OFF = 0
    PARALYZER = 1
    ELIMINATOR = 2


# Represents the sibyl-dominator judgement and execution system
# contains a set of records on recent evaluations and weapon status
class SibylSystem(object):
    def __init__(self, record_size=64, record_ttl=100) -> None:
        self.records = TTLCache(record_size, ttl=record_ttl)
        self.last_target = None
        self.safety_status = DominatorStatus.OFF

    def get_coefficient(self, target: str) -> int:
        if target in self.records:
            coefficient = self.records.get(target)
        else:
            coefficient = SibylSystem.calculate_coefficient(target)
            self.records[target] = coefficient
        return coefficient

    @staticmethod
    def is_separate_jurisdiction(target: str) -> bool:
        # can sibyl judge itself? Yes, yes she can.
        return target.strip().lower() in [
            "syraleaf!",
            "replay value",
            "tzhou",
        ]

    @staticmethod
    def is_criminally_asymptotic(target: str) -> bool:
        return target.strip().lower() in [
            "tzhou",
            "syraleaf!",
            "replay value",
            # due to someone's misspelling
            "sibyl",
            "sybil",
        ]

    @staticmethod
    def is_inherently_evil(target: str) -> bool:
        return target.strip().lower() in ["amadeus"]

    @staticmethod
    def calculate_coefficient(target) -> int:
        if SibylSystem.is_criminally_asymptotic(target):
            return 0
        elif SibylSystem.is_inherently_evil(target):
            return random.randint(301, 500)
        else:
            # usually safe
            if random.randint(1, 5) <= 4:
                return random.randint(0, 100)
            else:
                return random.randint(101, 500)

    # returns a number for lethality, and a string for announcement
    def dominator_decision(self, target: str) -> str:
        coefficient = self.get_coefficient(target)
        self.last_target = target
        response = None
        if SibylSystem.is_separate_jurisdiction(target):
            self.safety_status = DominatorStatus.OFF
            response = f"Target '{target}' is not under current jurisdiction."
        else:
            response = f"Target '{target}' has a crime coefficent of {coefficient}. "
            if coefficient == 0:
                response += "Target is literally a fucking saint."
                self.safety_status = DominatorStatus.OFF
            elif coefficient < 100:
                response += (
                    "Not a target for enforcement action, the trigger will be locked."
                )
                self.safety_status = DominatorStatus.OFF
            elif coefficient < 300:
                response += (
                    "They're a target for enforcement action. Enforcement Mode"
                    " is Paralyzer. The safety will be released."
                )
                self.safety_status = DominatorStatus.PARALYZER
            elif coefficient == 500:
                response += (
                    "They're a target for enforcement action. Enforcement Mode"
                    " is Atomic Disassembler. Like, dude, how bad can you be?"
                )
                self.safety_status = DominatorStatus.ELIMINATOR
            else:
                response += (
                    "They're a target for enforcement action. Enforcement Mode"
                    " is Lethal Eliminator. Aim Carefully and Eliminate the Target."
                )
                self.safety_status = DominatorStatus.ELIMINATOR
        return response

    # BOOOOM
    def dominator_fire(self) -> str:
        response = None
        if not self.last_target or self.safety_status == DominatorStatus.OFF:
            response = "Dominator is locked."
        elif self.safety_status == DominatorStatus.PARALYZER:
            del self.records[self.last_target]
            response = (
                f"\\> {self.last_target} <: https://gfycat.com/scarcejoyousfinwhale"
            )
        else:
            del self.records[self.last_target]
            response = (
                f"\\> {self.last_target}< : https://gfycat.com/regulartarthorseshoecrab"
            )
        self.last_target = None
        self.safety_status = DominatorStatus.OFF
        return response

    def dominator_force(self, target, value) -> None:
        self.records[target] = value
