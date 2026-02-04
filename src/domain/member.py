"""Entité Member - Domaine pur."""

from datetime import datetime


class Member:
    """Représente un membre de la bibliothèque (entité du domaine)."""
    
    def __init__(self, id: str, name: str, email: str, registered_at: datetime | None = None):
        # Validation dans le constructeur
        if not name or len(name) < 2:
            raise ValueError("Le nom doit contenir au moins 2 caractères")
        
        if not email or '@' not in email:
            raise ValueError("Adresse email invalide")
        
        self.id = id
        self.name = name
        self.email = email
        self.registered_at = registered_at
