import typing as t
from saas.core.security.rules import Rule as SecurityRule
from saas.core.mail import BaseMailProvider as MailProvider
from saas.domain.providers import BaseProvider as DomainProvider


class TypedSite(t.TypedDict):
    name: str
    url: str
    icon: str
    copyright: str


class TypedProvider(t.TypedDict):
    backend: str
    options: t.Dict[str, t.Any]


class Settings:
    SITE: TypedSite
    TENANT_ID_HEADER: str

    PERMISSION_NAME_FORMATTER: str
    DEFAULT_REGION: t.Optional[str]

    MAIL_PROVIDERS: t.Dict[str, MailProvider]
    PASSWORDLESS: bool
    SIGNUP_SECURITY_RULES: t.List[SecurityRule]
    RESET_PASSWORD_SECURITY_RULES: t.List[SecurityRule]

    # sso app
    SSO_PROVIDERS: t.List[TypedProvider]

    # domain app
    DOMAIN_PROVIDERS: t.Dict[str, DomainProvider]

    # billing app
    TRIAL_DAYS: int
    ALLOW_MULTIPLE_SUBSCRIPTIONS: bool
    STRIPE_API_KEY: str
    STRIPE_WEBHOOK_SECRET: str
    STRIPE_DEFAULT_CURRENCY: str
    STRIPE_DEFAULT_COUPON: t.Optional[str]

    # internal properties
    settings_key: str
    user_settings: t.Dict[str, t.Any]
    _cached_attrs: t.Set[str]

    def __init__(
        self,
        settings_key: t.Optional[str] = 'SAAS',
        user_settings: t.Optional[t.Dict[str, t.Any]] = None,
        defaults: t.Optional[t.Dict[str, t.Any]] = None,
    ) -> "Settings":
        ...

    def reload(self, value: t.Optional[t.Dict[str, t.Any]] = None):
        ...

    def listen_setting_changed(self, setting: str, **kwargs):
        ...


def perform_import_provider(data: TypedProvider):
    ...


def perform_import(val: t.Union[t.List[TypedProvider], t.Dict[str, TypedProvider], TypedProvider]):
    ...


saas_settings: Settings
