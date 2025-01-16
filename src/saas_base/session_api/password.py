from email.utils import formataddr
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from ..drf.views import Endpoint
from ..settings import saas_settings
from ..models import UserEmail
from ..security import check_security_rules
from ..services.notification import send_notification_mail, render_email_message
from ..serializers.password import (
    PasswordForgetSerializer,
    PasswordResetSerializer,
)


class PasswordForgotEndpoint(Endpoint):
    email_template_id = "reset_password"
    email_subject = _("Password Reset Request")

    permission_classes = []
    throttle_classes = [AnonRateThrottle]
    serializer_class = PasswordForgetSerializer

    def send_mail(self, request: Request, obj: UserEmail, code: str):
        user: AbstractUser = obj.user
        context = {"code": code, "site": saas_settings.SITE, "user": user}
        text_message, html_message = render_email_message(
            request._request,
            template_id=self.email_template_id,
            context=context,
        )
        name = user.get_full_name() or user.get_username()
        recipients = [formataddr((name, obj.email))]
        send_notification_mail(
            self.email_subject,
            recipients,
            text_message,
            html_message,
        )

    def post(self, request: Request):
        """Send a forgot password reset email code."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj: UserEmail = serializer.save()

        # check bad request rules
        check_security_rules(saas_settings.RESET_PASSWORD_SECURITY_RULES, request)

        code = serializer.save_password_code(obj)
        self.send_mail(request, obj, code)
        return Response('', status=204)


class PasswordResetEndpoint(Endpoint):
    permission_classes = []
    throttle_classes = [AnonRateThrottle]
    serializer_class = PasswordResetSerializer

    def post(self, request: Request):
        """Reset password of a user with the given code."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"next": settings.LOGIN_URL})
