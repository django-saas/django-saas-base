from django.apps import AppConfig


class DemoConfig(AppConfig):
    name = 'tests.demo_app'

    def ready(self):
        from saas_base.endpoints.user import UserEndpoint
        from tests.demo_app.serializers import UserSerializer

        UserEndpoint.serializer_class = UserSerializer
