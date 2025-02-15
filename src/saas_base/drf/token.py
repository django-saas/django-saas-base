import typing as t
from abc import ABCMeta
from django.contrib.auth.models import User as AuthUser
from ..models import get_tenant_model, Tenant, Member


class AbstractToken(metaclass=ABCMeta):
    scope: str
    tenant_id: t.Any
    user: AuthUser

    def get_tenant(self) -> Tenant:
        return get_tenant_model().objects.get_from_cache_by_pk(self.tenant_id)

    def get_all_permissions(self) -> t.Optional[t.Set[str]]:
        try:
            member = Member.objects.get_by_natural_key(self.tenant_id, self.user.pk)
            if member.is_active:
                return member.get_all_permissions()
        except Member.DoesNotExist:
            return None

    def check_permissions(self, resource_permissions: t.List[str]) -> bool:
        if not self.tenant_id or not self.user:
            return False

        if not self.user.is_active:
            return False

        if self.user.is_superuser:
            return True

        # tenant owner has full permission
        tenant = self.get_tenant()
        if tenant.owner_id == self.user.pk:
            return True

        perms = self.get_all_permissions()
        if not perms:
            return False

        for name in resource_permissions:
            if name in perms:
                return True
        return False

    def check_scopes(self, resource_scopes: t.List[str]):
        if self.scope == "__all__":
            return True

        token_scopes = set(self.scope.split())
        for rs in resource_scopes:
            if set(rs.split()).issubset(token_scopes):
                return True
        return False


class AuthToken(AbstractToken):
    scope = "__all__"

    def __init__(self, user=None, tenant_id=None):
        self.user = user
        self.tenant_id = tenant_id
