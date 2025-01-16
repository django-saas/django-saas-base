import typing as t
from saas.settings import saas_settings
from .base import BaseMailProvider
from .django import DjangoMailProvider


def get_mail_provider(name: str = 'default', fallback: t.Optional[str] = None):
    if name in saas_settings.MAIL_PROVIDERS:
        return saas_settings.MAIL_PROVIDERS[name]
    if fallback:
        return saas_settings.MAIL_PROVIDERS[fallback]


__all__ = ['get_mail_provider', 'BaseMailProvider', 'DjangoMailProvider']
