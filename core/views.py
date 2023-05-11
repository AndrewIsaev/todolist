from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.exceptions import AuthenticationFailed
from core.models import User
from core.serializers import (
    CreateUserSerializer,
    ProfileSerializer,
    LoginSerializer,
    UpdatePasswordSerializer,
)
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class SingUpView(generics.GenericAPIView):
    """
    Sing up view
    """

    serializer_class = CreateUserSerializer

    def post(self, request: Request, *args: tuple, **kwargs) -> Response:
        """
        Create user
        :param request: request
        :param args: args
        :param kwargs: kwargs
        :return: response
        """
        serializer: Serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = User.objects.create_user(**serializer.data)
        return Response(ProfileSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    """
    Login view
    """

    serializer_class = LoginSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        """
        User authentication
        :param request: request
        :param args: args
        :param kwargs: kwargs
        :return: response
        """
        serializer: Serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password'],
        )

        if not user:
            raise AuthenticationFailed

        login(request=request, user=user)
        return Response(ProfileSerializer(user).data, status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveUpdateDestroyAPIView):
    """
    Profile view
    """

    serializer_class = ProfileSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self) -> User:
        """
        Get user object from request
        :return: user
        """
        return self.request.user

    def delete(self, request, *args, **kwargs) -> status.HTTP_204_NO_CONTENT:
        """Logout"""
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdatePasswordView(generics.GenericAPIView):
    """
    Update password view
    """

    serializer_class = UpdatePasswordSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def put(self, request: Request, *args, **kwargs) -> Response:
        """
        Update password
        :param request: request
        :param args: args
        :param kwargs: kwargs
        :return: response
        """
        serializer: Serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user: User = request.user

        if not user.check_password(serializer.validated_data['old_password']):
            raise AuthenticationFailed('Incorrect password')

        user.set_password(serializer.validated_data['new_password'])
        user.save(update_fields=['password'])

        return Response(serializer.data)
