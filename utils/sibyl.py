"""Module for the dominator system."""
import enum
import random
from typing import Optional

from cachetools import TTLCache

SIBYL_RESPONSE_NOT_A_TARGET = (
    "Not a target for enforcement action, the trigger will be locked."
)
SIBYL_RESPONSE_PARALYZE = (
    "They're a target for enforcement action. Enforcement Mode"
    " is Paralyzer. The safety will be released."
)
SIBYL_RESPONSE_ELIMINATE = (
    "They're a target for enforcement action. Enforcement Mode"
    " is Lethal Eliminator. Aim Carefully and Eliminate the Target."
)


class DominatorStatus(enum.Enum):
    """Represents the states that the dominator can be in."""

    OFF = 0
    PARALYZER = 1
    ELIMINATOR = 2


class SibylSystem(object):
    """
    Represents the sibyl-dominator judgement and execution system.

    Contains a set of records on recent evaluations and weapon status
    """

    def __init__(self, record_size=64, record_ttl=100) -> None:
        """Create a SibylSystem object.

        Keyword Arguments:
            record_size {int} -- The number of records to cache. (default: {64})
            record_ttl {int} -- The time-to-live for records, in seconds
                (default: {100})
        """
        self.records = TTLCache(record_size, ttl=record_ttl)
        self.last_target: Optional[str] = None
        self.safety_status = DominatorStatus.OFF

    def get_coefficient(self, target: str) -> int:
        """Get coefficient of target, potentially from cache.

        Arguments:
            target {str} -- Name of the target.

        Returns:
            int -- target's crime coefficient.

        """
        if target in self.records:
            coefficient = self.records.get(target)
        else:
            coefficient = SibylSystem.calculate_coefficient(target)
            self.records[target] = coefficient
        return coefficient

    @staticmethod
    def is_separate_jurisdiction(target: str) -> bool:
        """Whether target is not judgeable."""
        return target.strip().lower() in [
            "syraleaf!",
            "replay",
            "tzhou",
        ]

    @staticmethod
    def is_criminally_asymptomatic(target: str) -> bool:
        """Whether target is always innocent."""
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
        """Whether target is always guilty."""
        return target.strip().lower() in ["amadeus"]

    @staticmethod
    def calculate_coefficient(target: str) -> int:
        """Calculate the crime coefficient of the target.

        Arguments:
            target {str} -- Target name.

        Returns:
            int -- crime coefficient.

        """
        if SibylSystem.is_criminally_asymptomatic(target):
            return 0
        elif SibylSystem.is_inherently_evil(target):
            return random.randint(301, 500)
        else:
            # usually safe
            if random.randint(1, 5) <= 4:
                return random.randint(0, 100)
            else:
                return random.randint(101, 500)

    def dominator_decision(self, target: str) -> str:
        """Determine message for target judgement.

        Arguments:
            target {str} -- Target name.

        Returns:
            str -- The decision message from Sibyl.

        """
        coefficient = self.get_coefficient(target)
        self.last_target = target
        response = None
        if SibylSystem.is_separate_jurisdiction(target):
            self.safety_status = DominatorStatus.OFF
            response = f"Target '{target}' is not under current jurisdiction."
        else:
            response = f"Target '{target}' has a crime coefficient of {coefficient}. "
            if coefficient == 0:
                response += "Target is literally a fucking saint."
                self.safety_status = DominatorStatus.OFF
            elif coefficient < 100:
                response += SIBYL_RESPONSE_NOT_A_TARGET
                self.safety_status = DominatorStatus.OFF
            elif coefficient < 300:
                response += SIBYL_RESPONSE_PARALYZE
                self.safety_status = DominatorStatus.PARALYZER
            else:
                response += SIBYL_RESPONSE_ELIMINATE
                self.safety_status = DominatorStatus.ELIMINATOR
        return response

    # BOOOOM
    def dominator_fire(self) -> str:
        """Determine message when firing upon the last scanned target.

        Returns:
            str -- The firing message.

        """
        response = None
        if not self.last_target or self.safety_status == DominatorStatus.OFF:
            response = "Dominator is locked."
        elif self.safety_status == DominatorStatus.PARALYZER:
            response = f"{self.last_target}: https://gfycat.com/scarcejoyousfinwhale"
            del self.records[self.last_target]
        else:
            response = (
                f"{self.last_target}: https://gfycat.com/regulartarthorseshoecrab"
            )
            del self.records[self.last_target]
        self.last_target = None
        self.safety_status = DominatorStatus.OFF
        return response

    def dominator_force(self, target: str, value: int) -> None:
        """Set the criminal coefficient of a target by force.

        Arguments:
            target {str} -- Target name.
            value {int} -- Desired criminal coefficient.
        """
        self.records[target] = value
