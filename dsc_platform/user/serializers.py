from .models import User
from rest_framework import serializers
from .utils import validate_password, validate_phone_number


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['groups', 'user_permissions', ]

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
        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
