"""Port MemberRepository - Interface pour la persistance des membres."""

from abc import ABC, abstractmethod
from typing import List
from domain.member import Member


class MemberRepository(ABC):
    """Interface définissant les opérations de persistance pour Member."""
    
    @abstractmethod
    def save(self, member: Member) -> None:
        """Sauvegarde un membre."""
        pass
    
    @abstractmethod
    def get_by_id(self, member_id: str) -> Member | None:
        """Récupère un membre par son ID."""
        pass
    
    @abstractmethod
    def list_all(self) -> List[Member]:
        """Liste tous les membres."""
        pass
    
    @abstractmethod
    def count(self) -> int:
        """Compte le nombre total de membres."""
        pass
