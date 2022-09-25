"""Django app."""
from django.apps import AppConfig


class PollsConfig(AppConfig):
    """App config."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'polls'
