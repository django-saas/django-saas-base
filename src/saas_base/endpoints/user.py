from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin
from ..drf.views import AuthenticatedEndpoint
from ..models import Member
from ..serializers.user import (
    UserSerializer,
    UserPasswordSerializer,
)
from ..serializers.member import UserTenantsSerializer

__all__ = [
    'UserEndpoint',
    'UserPasswordEndpoint',
    'UserTenantsEndpoint',
]


class UserEndpoint(AuthenticatedEndpoint):
    resource_scopes = ['user', 'user:profile']
    serializer_class = UserSerializer

    def get(self, request: Request):
        """Retrieve current user information."""
        serializer: UserSerializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """Update current user information."""
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class UserPasswordEndpoint(AuthenticatedEndpoint):
    resource_scopes = ['user:password']
    serializer_class = UserPasswordSerializer

    def post(self, request: Request, *args, **kwargs):
        """Update current user's password"""
        serializer: UserPasswordSerializer = self.get_serializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=204)


class UserTenantsEndpoint(ListModelMixin, AuthenticatedEndpoint):
    serializer_class = UserTenantsSerializer
    queryset = Member.objects.select_related('tenant').all()

    def filter_queryset(self, queryset):
        status = self.request.query_params.get('status')
        queryset = queryset.prefetch_related('groups', 'permissions', 'groups__permissions')
        queryset = queryset.filter(user=self.request.user)

        if status == 'all':
            return queryset.all()
        if status == 'waiting':
            queryset = queryset.filter(status=Member.InviteStatus.WAITING)
        else:
            queryset = queryset.filter(status=Member.InviteStatus.ACTIVE)
        return queryset.all()

    def get(self, request: Request, *args, **kwargs):
        """List all the current user's tenants."""
        return self.list(request, *args, **kwargs)
