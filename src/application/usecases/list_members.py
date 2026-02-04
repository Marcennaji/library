"""Use case : Lister les membres."""

from typing import List
from domain.member import Member
from ports.member_repository import MemberRepository


class ListMembersUseCase:
    """Cas d'usage pour lister les membres."""
    
    def __init__(self, member_repository: MemberRepository):
        self.member_repository = member_repository
    
    def execute(self) -> List[Member]:
        """Liste tous les membres."""
        return self.member_repository.list_all()
