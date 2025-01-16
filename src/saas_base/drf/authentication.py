from rest_framework.request import Request
from rest_framework.authentication import (
    SessionAuthentication as _SessionAuthentication,
)
from .token import AuthToken


class SessionAuthentication(_SessionAuthentication):
    def authenticate(self, request: Request):
        tenant_id = getattr(request._request, "tenant_id", None)
        credentials = super().authenticate(request)
        if credentials is None:
            return None
        user = credentials[0]
        token = AuthToken(user, tenant_id)
        return user, token
