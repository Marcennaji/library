"""Générateur d'IDs fixe pour les tests."""

from ports.id_generator import IDGenerator


class FixedIDGenerator(IDGenerator):
    """Générateur d'IDs prévisibles pour les tests."""
    
    def __init__(self):
        self._book_counter = 0
        self._member_counter = 0
        self._loan_counter = 0
    
    def generate_book_id(self) -> str:
        """Génère un ID pour un livre (TEST-B1, TEST-B2...)."""
        self._book_counter += 1
        return f"TEST-B{self._book_counter}"
    
    def generate_member_id(self) -> str:
        """Génère un ID pour un membre (TEST-M1, TEST-M2...)."""
        self._member_counter += 1
        return f"TEST-M{self._member_counter}"
    
    def generate_loan_id(self) -> str:
        """Génère un ID pour un emprunt (TEST-L1, TEST-L2...)."""
        self._loan_counter += 1
        return f"TEST-L{self._loan_counter}"
