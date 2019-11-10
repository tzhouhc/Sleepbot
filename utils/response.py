"""Handle the default response/easter egg mechanism."""
import re
from typing import Optional

from .data import EasterEgg, EasterHen


class ResponseManager(object):
    """Manager for easter egg responses."""

    def __init__(self) -> None:
        """Create a response manager."""
        self.hen: EasterHen

    def set_hen(self, hen: EasterHen) -> None:
        """Set the EasterHen for the Response Manager.

        Arguments:
            hen {EasterHen} -- The provider of easter eggs.
        """
        self.hen = hen

    def refresh(self) -> None:
        """Instruct the hen to fetch latest eggs."""
        self.hen.refresh()

    def get_triggered_egg(self, message_text: str) -> Optional[EasterEgg]:
        """Obtain the egg that would be triggered by the message.

        Arguments:
            message_text {str} -- The message to test against.

        Returns:
            Optional[EasterEgg] -- The easter egg that the message triggered.

        """
        for egg in self.hen.get_eggs():
            if egg.trigger_on_str(message_text.strip().lower()):
                return egg
        return None
