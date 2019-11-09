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

    def get_triggered_eggs(self, message_text: str) -> Optional[EasterEgg]:
        for egg in self.hen.get_eggs():
            if egg.trigger_on_str(message_text.strip().lower()):
                return egg
        return None
