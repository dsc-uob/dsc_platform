from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """User serializer class,"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password',
                  'first_name', 'last_name', 'gender',
                  'stage', 'bio', 'is_active', 'is_staff',
                  'is_superuser', 'last_login', 'photo')
        read_only_fields = ('last_login', 'is_active', 'is_staff',
                            'is_superuser', 'photo')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 6
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


class AuthTokenSerializer(serializers.Serializer):
    """Auth token serializer."""

    def update(self, instance, validated_data):
        raise NotImplementedError('`update()` must be implemented.')

    def create(self, validated_data):
        raise NotImplementedError('`create()` must be implemented.')

    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate of user."""
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )

        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs


class UserPhotoSerializer(serializers.ModelSerializer):
    """Serializer for uploading user photo."""

    class Meta:
        model = get_user_model()
        fields = ('id', 'photo')
        read_only_fields = ('id',)
