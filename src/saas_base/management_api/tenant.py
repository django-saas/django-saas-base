from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, ListModelMixin
from rest_framework.request import Request
from saas.drf.views import Endpoint, TenantEndpoint
from saas.core.models import get_tenant_model, Member
from saas.core.serializers.tenant import TenantSerializer
from saas.core.serializers.member import MemberDetailSerializer


class SelectedTenantEndpoint(RetrieveModelMixin, TenantEndpoint):
    serializer_class = TenantSerializer
    resource_name = 'tenant'
    tenant_id_field = "pk"

    def get_queryset(self):
        return get_tenant_model().objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        obj = self.get_object_or_404(queryset)
        self.check_object_permissions(self.request, obj)
        return obj

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CurrentMemberEndpoint(RetrieveModelMixin, TenantEndpoint):
    queryset = Member.objects.all()
    serializer_class = MemberDetailSerializer
    resource_name = 'tenant'

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        return self.get_object_or_404(queryset, user=self.request.user)

    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class TenantsEndpoint(CreateModelMixin, ListModelMixin, Endpoint):
    serializer_class = TenantSerializer

    def get_queryset(self):
        return get_tenant_model().objects.filter(owner=self.request.user).all()

    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
