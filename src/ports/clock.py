"""Port Clock - Interface pour l'abstraction du temps."""

from abc import ABC, abstractmethod
from datetime import datetime


class Clock(ABC):
    """Interface pour obtenir l'heure actuelle (permet les tests)."""
    
    @abstractmethod
    def now(self) -> datetime:
        """Retourne la date et heure actuelle."""
        pass
