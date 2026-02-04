"""Utilitaire de connexion à la base de données."""

import sqlite3


def get_connection():
    """Retourne une connexion à la base de données SQLite."""
    return sqlite3.connect("library.db")
