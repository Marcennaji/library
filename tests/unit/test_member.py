"""Tests unitaires de l'entité Member."""

import pytest
from datetime import datetime
from domain.member import Member


def test_member_creation_valid():
    """Test : création d'un membre valide."""
    member = Member(
        id="M1",
        name="Alice Dupont",
        email="alice@example.com",
        registered_at=datetime(2025, 1, 1)
    )
    
    assert member.id == "M1"
    assert member.name == "Alice Dupont"
    assert member.email == "alice@example.com"


def test_member_creation_invalid_name():
    """Test : création d'un membre avec nom invalide."""
    with pytest.raises(ValueError, match="au moins 2 caractères"):
        Member("M1", "A", "alice@example.com")


def test_member_creation_invalid_email():
    """Test : création d'un membre avec email invalide."""
    with pytest.raises(ValueError, match="email invalide"):
        Member("M1", "Alice", "invalid-email")
    
    with pytest.raises(ValueError, match="email invalide"):
        Member("M1", "Alice", "")
