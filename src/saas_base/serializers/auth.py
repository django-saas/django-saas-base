import random
import string
import typing as t
from django.db import transaction
from django.core.cache import cache
from django.utils.translation import gettext as _
from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from ..models import UserEmail

SIGNUP_CODE = 'saas:signup_code'


class EmailCode:
    def __init__(self, email: str, code: str):
        self.email = email
        self.code = code


class SignupCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, email: str):
        try:
            UserEmail.objects.get(email=email)
            raise ValidationError(_("This email address is already associated with an existing account."))
        except UserEmail.DoesNotExist:
            return email

    def create(self, validated_data) -> EmailCode:
        email = validated_data["email"]
        code = ''.join(random.sample(string.ascii_uppercase, 6))
        cache_key = f"{SIGNUP_CODE}:{email}:{code}"
        cache.set(cache_key, 1, timeout=300)
        return EmailCode(email, code)


class SignupPasswordSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, validators=[UnicodeUsernameValidator()])
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True, max_length=6)
    password = serializers.CharField(required=True)

    def validate_username(self, username: str):
        cls: t.Type[AbstractUser] = get_user_model()
        try:
            cls.objects.get(username=username)
            raise ValidationError(_("This username is already associated with an existing account."))
        except cls.DoesNotExist:
            return username

    def validate_password(self, raw_password: str):
        password_validation.validate_password(raw_password)
        return raw_password

    def validate_code(self, code: str):
        email = self.initial_data["email"]
        code = code.upper()
        cache_key = f"{SIGNUP_CODE}:{email}:{code}"
        has_code: str = cache.get(cache_key)
        if not has_code:
            raise ValidationError(_("Code does not match or expired."))
        return code

    def create(self, validated_data) -> AbstractUser:
        username = validated_data["username"]
        email = validated_data["email"]
        password = validated_data["password"]
        cls: t.Type[AbstractUser] = get_user_model()
        with transaction.atomic():
            user = cls.objects.create_user(username=username, email=email, password=password)
            UserEmail.objects.create(user=user, email=email, primary=True, verified=True)

        code = validated_data["code"]
        cache_key = f"{SIGNUP_CODE}:{email}:{code}"
        cache.delete(cache_key)
        return user
