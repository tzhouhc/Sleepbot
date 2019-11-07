import re
from typing import Optional

from .data import EasterEgg, EasterHen


class ResponseManager(object):
    def __init__(self) -> None:
        self.hen: EasterHen

    def set_hen(self, hen: EasterHen) -> None:
        self.hen = hen

    def refresh(self) -> None:
        self.hen.refresh()

    @classmethod
    def should_operate_on_strings(
        cls, operator: str, sub_operand: str, operand: str
    ) -> bool:
        if operator == "match":
            return sub_operand == operand
        elif operator == "contains_word":
            return re.search(fr"\b{sub_operand}\b", operand) is not None
        elif operator == "prefix":
            return operand.startswith(sub_operand)
        elif operator == "suffix":
            return operand.endswith(sub_operand)
        elif operator == "contains":
            return sub_operand in operand
        elif operator == "regex":
            return re.search(fr"{sub_operand}", operand) is not None
        else:  # operator not recognized
            # TODO: do actual logging instead of stdout print
            print(f"operator '{operator}' not recognized.")
            return False

    def get_triggered_eggs(self, message_text: str) -> Optional[EasterEgg]:
        for egg in self.hen.get_eggs():
            if self.should_operate_on_strings(
                egg.operator, egg.keyword, message_text.strip().lower()
            ):
                return egg
        return None
