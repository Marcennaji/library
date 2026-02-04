"""Fonctions utilitaires pour les dates."""

from datetime import datetime, timedelta


def get_current_datetime():
    """Retourne la date et heure actuelle."""
    return datetime.now()


def add_days(date, days):
    """Ajoute des jours à une date."""
    return date + timedelta(days=days)


def format_date(date, format_string='%d/%m/%Y'):
    """Formate une date en chaîne de caractères."""
    return date.strftime(format_string)
