from django.urls import path, include
from drf_spectacular.views import SpectacularJSONAPIView


urlpatterns = [
    path('m/', include('saas_base.management_api.urls')),
    path('s/', include('saas_base.session_api.urls')),
    path('schema/openapi', SpectacularJSONAPIView.as_view(), name='schema'),
]
