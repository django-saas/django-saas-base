from django.urls import path, include

urlpatterns = [
    path('m/', include('saas_base.management_api.urls')),
    path('s/', include('saas_base.session_api.urls')),
    path('debug_emails/', include('saas_base.debug_emails.urls')),
]
