from django.urls import path, include
from saas.billing_stripe.webhook import StripeWebhookView

urlpatterns = [
    path('m/', include('saas.core.management_api.urls')),
    path('s/', include('saas.core.session_api.urls')),
    path('m/', include('saas.domain.management_api.urls')),
    path('m/', include('saas.sso.management_api.urls')),
    path('s/', include('saas.sso.management_views.urls')),
    path('m/billing/', include('saas.billing.management_api.urls')),
    path('m/stripe/', include('saas.billing_stripe.management_api.urls')),
    path('m/stripe/webhook', StripeWebhookView.as_view()),
]
