from django.db.models import Q
from rest_framework.mixins import (
    RetrieveModelMixin,
    CreateModelMixin,
    UpdateModelMixin,
    ListModelMixin,
)
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from ..drf.views import AuthenticatedEndpoint, TenantEndpoint
from ..models import get_tenant_model, Member
from ..serializers.tenant import TenantSerializer, TenantUpdateSerializer

__all__ = [
    'SelectedTenantEndpoint',
    'TenantListEndpoint',
    'TenantItemEndpoint',
]


class SelectedTenantEndpoint(RetrieveModelMixin, TenantEndpoint):
    serializer_class = TenantSerializer
    resource_name = 'tenant'
    tenant_id_field = 'pk'

    def get_queryset(self):
        return get_tenant_model().objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = self.get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class TenantListEndpoint(CreateModelMixin, ListModelMixin, AuthenticatedEndpoint):
    serializer_class = TenantSerializer
    queryset = get_tenant_model().objects.all()
    pagination_class = None
    permission_classes = [IsAuthenticated] + api_settings.DEFAULT_PERMISSION_CLASSES

    def get_queryset(self):
        default_query = Q(owner=self.request.user)
        query_filter = self.request.query_params.get('filter', 'created')
        if query_filter == 'all':
            query = default_query | Q(member__user=self.request.user)
        elif query_filter == 'active':
            query = default_query | Q(member__user=self.request.user, member__status=Member.InviteStatus.ACTIVE)
        elif query_filter == 'pending':
            query = Q(member__user=self.request.user, member__status=Member.InviteStatus.WAITING)
        else:
            query = default_query
        return self.queryset.filter(query).all()

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TenantItemEndpoint(RetrieveModelMixin, UpdateModelMixin, TenantEndpoint):
    serializer_class = TenantUpdateSerializer
    queryset = get_tenant_model().objects.all()
    filter_backends = []
    resource_name = 'tenant'
    tenant_id_field = 'pk'

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request: Request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
