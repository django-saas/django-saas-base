from django.urls import path, include
from django.contrib.staticfiles.urls import urlpatterns as static_urlpatterns
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path('api/', include('saas_base.management_api.urls')),
    path('session/', include('saas_base.session_api.urls')),
    path('debug_emails/', include('saas_base.debug_emails.urls')),

    path('schema/openapi', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
] + static_urlpatterns
