from django.conf import settings
from django.core.signals import setting_changed
from django.utils.module_loading import import_string


DEFAULTS = {
    'SITE': {
        'name': 'SaaS',
        'url': '',
        'icon': '',
        'copyright': '© 2023',
    },
    'TENANT_ID_HEADER': 'X-Tenant-Id',

    'DB_CACHE_ALIAS': 'default',
    'PERMISSION_NAME_FORMATTER': '{resource}.{action}',

    # core app
    'DEFAULT_REGION': None,
    'MAIL_PROVIDERS': {
        'default': {
            'backend': 'saas.core.mail.DjangoMailProvider',
            'options': {},
        },
    },
    'SIGNUP_SECURITY_RULES': [],
    'RESET_PASSWORD_SECURITY_RULES': [],
    'DEFAULT_MAIL_FROM': None,
    'PASSWORDLESS': False,

    # sso app
    'SSO_PROVIDERS': [],

    # domain app
    'DOMAIN_PROVIDERS': {},

    # billing app
    'TRIAL_DAYS': 7,
    'ALLOW_MULTIPLE_SUBSCRIPTIONS': False,
    'STRIPE_API_KEY': '',
    'STRIPE_WEBHOOK_SECRET': '',
    'STRIPE_DEFAULT_CURRENCY': 'usd',
    'STRIPE_DEFAULT_COUPON': None,
}


class Settings:
    IMPORT_PROVIDERS = [
        'MAIL_PROVIDERS',
        'SIGNUP_SECURITY_RULES',
        'RESET_PASSWORD_SECURITY_RULES',
        'DOMAIN_PROVIDERS',
    ]

    def __init__(self, settings_key="SAAS", user_settings=None, defaults=None):
        self.settings_key = settings_key
        self._user_settings = user_settings
        if defaults is None:
            defaults = DEFAULTS
        self.defaults = defaults
        self._cached_attrs = set()

    @property
    def user_settings(self):
        if self._user_settings is None:
            self._user_settings = getattr(settings, self.settings_key, {})
        return self._user_settings

    def __getitem__(self, attr):
        try:
            val = self.user_settings[attr]
        except KeyError:
            val = self.defaults[attr]
        return val

    def __getattr__(self, attr):
        if attr not in self.defaults:
            raise AttributeError("Invalid %s setting: '%s'" % (self.settings_key, attr))

        val = self[attr]

        # Coerce import strings into classes
        if attr in self.IMPORT_PROVIDERS:
            val = perform_import(val)

        # Cache the result
        self._cached_attrs.add(attr)
        setattr(self, attr, val)
        return val

    def reload(self, value=None):
        for attr in self._cached_attrs:
            delattr(self, attr)

        self._cached_attrs.clear()
        if isinstance(value, dict):
            self.user_settings.update(value)
        else:
            self._user_settings = None

    def listen_setting_changed(self, setting, **kwargs):
        if setting == self.settings_key:
            self.reload(kwargs.get('value'))


def perform_import_provider(data):
    backend_cls = import_string(data['backend'])
    options = data.get('options', {})
    return backend_cls(**options)


def perform_import(val):
    if val is None:
        return None

    elif isinstance(val, (list, tuple)):
        return [perform_import_provider(item) for item in val]
    elif isinstance(val, dict) and 'backend' not in val:
        return {k: perform_import_provider(val[k]) for k in val}
    else:
        return perform_import_provider(val)


saas_settings = Settings()
setting_changed.connect(saas_settings.listen_setting_changed)
