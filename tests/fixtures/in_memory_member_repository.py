"""Repository Member en mémoire pour les tests."""

from typing import List
from domain.member import Member
from ports.member_repository import MemberRepository


class InMemoryMemberRepository(MemberRepository):
    """Implémentation en mémoire du repository de membres (pour tests)."""
    
    def __init__(self):
        self._members = {}
    
    def save(self, member: Member) -> None:
        """Sauvegarde un membre en mémoire."""
        self._members[member.id] = member
    
    def get_by_id(self, member_id: str) -> Member | None:
        """Récupère un membre par son ID."""
        return self._members.get(member_id)
    
    def list_all(self) -> List[Member]:
        """Liste tous les membres."""
        return list(self._members.values())
    
    def count(self) -> int:
        """Compte le nombre total de membres."""
        return len(self._members)
    
    def clear(self):
        """Vide le repository (utile entre les tests)."""
        self._members.clear()
