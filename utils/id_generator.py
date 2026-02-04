"""Générateur d'identifiants uniques."""

import uuid


def generate_id():
    """Génère un identifiant unique."""
    return str(uuid.uuid4())
