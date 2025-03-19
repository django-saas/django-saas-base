from django.urls import path
from ..endpoints.user import (
    UserEndpoint,
    UserPasswordEndpoint,
    UserTenantsEndpoint,
)

urlpatterns = [
    path('', UserEndpoint.as_view()),
    path('password/', UserPasswordEndpoint.as_view()),
    path('tenants/', UserTenantsEndpoint.as_view()),
]
