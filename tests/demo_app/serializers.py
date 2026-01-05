from django.contrib.auth import get_user_model
from rest_framework import serializers
from saas_base.drf.serializers import FlattenModelSerializer
from tests.demo_app.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ('user',)


class UserSerializer(FlattenModelSerializer):
    profile = UserProfileSerializer()
    name = serializers.CharField(source='get_full_name', read_only=True)

    class Meta:
        model = get_user_model()
        exclude = ['password', 'groups', 'user_permissions']
        flatten_fields = ['profile']
