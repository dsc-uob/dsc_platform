from django.contrib.auth import get_user_model
from rest_framework import serializers
from .utils import validate_password, validate_phone_number


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ['groups', 'user_permissions', 'is_deleted']
        read_only_fields = ('last_login', 'is_active', 'is_staff',
                            'is_superuser', 'photo')

        extra_kwargs = {
            'first_name': {
                'min_length': 3
            },
            'last_name': {
                'min_length': 3
            },
            'username': {
                'min_length': 3
            },
            'phone_number': {
                'validators': [
                    validate_phone_number
                ]
            },
            'password': {
                'write_only': True,
                'min_length': 6,
                'validators': [
                    validate_password,
                ]
            },
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
