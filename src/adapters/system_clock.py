"""Adaptateur Clock système."""

from datetime import datetime
from ports.clock import Clock


class SystemClock(Clock):
    """Implémentation utilisant l'horloge système."""
    
    def now(self) -> datetime:
        """Retourne l'heure système actuelle."""
        return datetime.now()
