from django.db.models.fields import BinaryField
from django.conf import settings
from saas.utils import crypto


class CryptoField(BinaryField):
    def to_python(self, value) -> bytes:
        value: bytes = super().to_python(value)
        keys = getattr(settings, "CRYPTO_FIELDS_KEYS", None)
        if keys is None:
            raise RuntimeError("Missing CRYPTO_FIELDS_KEYS in settings")
        return crypto.rotate_decrypt(ciphertext=value, keys=keys)

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def get_prep_value(self, value):
        if isinstance(value, str):
            value = value.encode("ascii")
        value = super().get_prep_value(value)
        keys = getattr(settings, "CRYPTO_FIELDS_KEYS", None)
        if keys is None:
            raise RuntimeError("Missing CRYPTO_FIELDS_KEYS in settings")
        key = keys[-1]
        return crypto.encrypt(value, key)
