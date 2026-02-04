"""Utilitaires de validation."""

import re


def validate_email(email):
    """Valide une adresse email."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_isbn(isbn):
    """Valide un ISBN (vérification basique)."""
    isbn_clean = isbn.replace("-", "").replace(" ", "")
    return len(isbn_clean) in [10, 13] and isbn_clean.isdigit()
