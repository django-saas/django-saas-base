from django.urls import path
from .tenant import (
    SelectedTenantEndpoint,
    CurrentMemberEndpoint,
    TenantsEndpoint,
)
from .members import (
    MemberListEndpoint,
    MemberItemEndpoint,
    MemberGroupsEndpoint,
    MemberGroupItemEndpoint,
    MemberPermissionsEndpoint,
    MemberPermissionItemEndpoint,
)
from .user import (
    UserEndpoint,
    UserPasswordEndpoint,
    UserEmailListEndpoint,
    UserTenantsEndpoint,
)

urlpatterns = [
    path('user', UserEndpoint.as_view()),
    path('user/password', UserPasswordEndpoint.as_view()),
    path('user/emails', UserEmailListEndpoint.as_view()),
    path('user/tenants', UserTenantsEndpoint.as_view()),

    path('tenants', TenantsEndpoint.as_view()),
    path('tenant', SelectedTenantEndpoint.as_view()),
    path('tenant/member', CurrentMemberEndpoint.as_view()),

    path('members', MemberListEndpoint.as_view()),
    path('members/<pk>', MemberItemEndpoint.as_view()),
    path('members/<member_id>/groups', MemberGroupsEndpoint.as_view()),
    path('members/<member_id>/permissions', MemberPermissionsEndpoint.as_view()),
    path('members/<member_id>/groups/<pk>', MemberGroupItemEndpoint.as_view()),
    path('members/<member_id>/permissions/<pk>', MemberPermissionItemEndpoint.as_view()),
]
