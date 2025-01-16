from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.auth import login, logout
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from ..drf.views import Endpoint
from ..settings import saas_settings
from ..security import check_security_rules
from ..services.notification import send_notification_mail, render_email_message
from ..serializers.auth import (
    EmailCode,
    SignupCodeSerializer,
    SignupPasswordSerializer,
)
from ..serializers.password import PasswordLoginSerializer
from ..signals import after_signup_user, after_login_user


class SignupCodeEndpoint(Endpoint):
    email_template_id = "signup_code"
    email_subject = _("Signup Request")
    authentication_classes = []
    permission_classes = []
    throttle_classes = [AnonRateThrottle]
    serializer_class = SignupCodeSerializer

    def send_mail(self, request: Request, user: EmailCode):
        # check spammer bots
        context = {"code": user.code, "site": saas_settings.SITE}
        text_message, html_message = render_email_message(
            request._request,
            template_id=self.email_template_id,
            context=context,
        )
        send_notification_mail(
            self.email_subject,
            [user.email],
            text_message,
            html_message,
        )

    def post(self, request: Request):
        """Send a sign-up code to user's email address."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj: EmailCode = serializer.save()

        # check bad request rules
        check_security_rules(saas_settings.SIGNUP_SECURITY_RULES, request)

        self.send_mail(request, obj)
        return Response('', status=204)


class AuthEndpoint(Endpoint):
    authentication_classes = []
    permission_classes = []
    throttle_classes = [AnonRateThrottle]

    def login_user(self, request: Request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request._request, user, 'django.contrib.auth.backends.ModelBackend')
        return user


class SignupConfirmEndpoint(AuthEndpoint):
    serializer_class = SignupPasswordSerializer

    def post(self, request: Request):
        """Register a new user and login."""
        user = self.login_user(request)
        after_signup_user.send(
            self.__class__,
            user=user,
            request=request._request,
            strategy="password",
        )
        return Response({"next": settings.LOGIN_REDIRECT_URL})


class PasswordLogInEndpoint(AuthEndpoint):
    serializer_class = PasswordLoginSerializer

    def post(self, request: Request):
        """Login a user with the given username and password."""
        user = self.login_user(request)
        after_login_user.send(
            self.__class__,
            user=user,
            request=request._request,
            strategy="password",
        )
        return Response({"next": settings.LOGIN_REDIRECT_URL})


class LogoutEndpoint(AuthEndpoint):
    def post(self, request: Request):
        """Clear the user session and log the user out."""
        logout(request._request)
        return Response({"next": settings.LOGIN_URL})
