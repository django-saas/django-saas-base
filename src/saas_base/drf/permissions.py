from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from saas.settings import saas_settings

__all__ = [
    'HasResourcePermission',
    'HasResourceScope',
]


http_method_actions = {
    'GET': 'read',
    'HEAD': 'read',
    'POST': 'write',
    'PUT': 'write',
    'PATCH': 'write',
    'DELETE': 'admin',
}


class HasResourcePermission(BasePermission):
    @staticmethod
    def get_resource_permissions(view, method):
        resource = getattr(view, 'resource_name', None)
        if not resource:
            return

        action = getattr(view, 'resource_action', None)
        if not action:
            method_actions = getattr(view, 'resource_http_method_actions', http_method_actions)
            action = method_actions.get(method)

        permission = saas_settings.PERMISSION_NAME_FORMATTER.format(
            resource=resource,
            action=action,
        )
        return [permission]

    def has_permission(self, request: Request, view):
        if not request.user or not request.user.is_active:
            return False
        resource_permissions = self.get_resource_permissions(view, request.method)
        if not resource_permissions:
            return True
        if request.auth and hasattr(request.auth, 'check_permissions'):
            return request.auth.check_permissions(resource_permissions)
        return False


class HasResourceScope(BasePermission):
    @staticmethod
    def get_resource_scopes(request, view):
        if hasattr(view, 'get_resource_scopes'):
            return view.get_resource_scopes(request)

    def has_permission(self, request: Request, view):
        if hasattr(view, 'get_resource_scopes'):
            resource_scopes = view.get_resource_scopes(request)
        elif hasattr(view, 'resource_scopes'):
            resource_scopes = view.resource_scopes
        else:
            resource_scopes = None

        if not resource_scopes:
            return True

        if request.auth and hasattr(request.auth, 'check_scopes'):
            return request.auth.check_scopes(resource_scopes)
        return False
