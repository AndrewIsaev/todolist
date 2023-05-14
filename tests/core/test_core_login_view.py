import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from core.models import User


@pytest.mark.django_db()
class TestUserLogin:
    url = reverse('core:login')

    def test_login(self, client):
        """
        Test login to application
        """
        user = User.objects.create_user(username='test_user', password='test_password')
        response: Response = client.post(
            self.url, data={'username': user.username, 'password': 'test_password'}
        )
        assert response.status_code == status.HTTP_200_OK
