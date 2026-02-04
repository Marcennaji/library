"""Entité Book - Domaine pur."""

from datetime import datetime


class Book:
    """Représente un livre dans la bibliothèque (entité du domaine)."""
    
    def __init__(self, id: str, title: str, author: str, isbn: str | None = None, 
                 status: str = "available", registered_at: datetime | None = None):
        # Validation dans le constructeur (invariants du domaine)
        if not title or len(title) < 2:
            raise ValueError("Le titre doit contenir au moins 2 caractères")
        
        if not author or len(author) < 2:
            raise ValueError("L'auteur doit contenir au moins 2 caractères")
        
        self.id = id
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status
        self.registered_at = registered_at
    
    def is_available(self) -> bool:
        """Vérifie si le livre est disponible pour emprunt (logique métier)."""
        return self.status == "available"
    
    def mark_as_borrowed(self):
        """Marque le livre comme emprunté (logique métier)."""
        if not self.is_available():
            raise ValueError(f"Le livre n'est pas disponible (statut: {self.status})")
        self.status = "borrowed"
    
    def mark_as_returned(self):
        """Marque le livre comme retourné (logique métier)."""
        self.status = "available"
