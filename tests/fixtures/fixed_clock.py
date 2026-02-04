"""Fixture Clock pour les tests."""

from datetime import datetime
from ports.clock import Clock


class FixedClock(Clock):
    """Clock avec une date/heure fixe pour les tests."""
    
    def __init__(self, fixed_time: datetime):
        self.fixed_time = fixed_time
    
    def now(self) -> datetime:
        """Retourne toujours la même date/heure."""
        return self.fixed_time
