from django.urls import path
from .views import (
    view_signup_code,
    view_reset_password,
)


urlpatterns = [
    path('signup_code.<suffix>', view_signup_code),
    path('reset_password.<suffix>', view_reset_password),
]
