"""Use case : Enregistrer un nouveau membre."""

from domain.member import Member
from ports.member_repository import MemberRepository
from ports.id_generator import IDGenerator
from ports.clock import Clock


class CreateMemberUseCase:
    """Cas d'usage pour enregistrer un nouveau membre."""
    
    def __init__(self, member_repository: MemberRepository, id_generator: IDGenerator, clock: Clock):
        self.member_repository = member_repository
        self.id_generator = id_generator
        self.clock = clock
    
    def execute(self, name: str, email: str) -> Member:
        """Crée et sauvegarde un nouveau membre."""
        member_id = self.id_generator.generate_member_id()
        registered_at = self.clock.now()
        
        member = Member(
            id=member_id,
            name=name,
            email=email,
            registered_at=registered_at
        )
        
        self.member_repository.save(member)
        return member
