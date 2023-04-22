from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'},
        validators=[
            validate_password,
        ],
        required=True,
        write_only=False,
    )
    password_repeat = serializers.CharField(
        style={'input_type': 'password'},
        validators=[
            validate_password,
        ],
        required=True,
        write_only=True,
    )

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password_repeat',
        )

    def validate(self, attrs: dict) -> dict | ValidationError:
        if attrs.get('password') != attrs.get('password_repeat'):
            return ValidationError('Passwords must match')
        return attrs


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})


class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        style={'input_type': 'password'}, required=True
    )
    new_password = serializers.CharField(
        style={'input_type': 'password'}, required=True
    )
