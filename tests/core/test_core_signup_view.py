import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response


@pytest.mark.django_db()
class TestUserCreate:
    url = reverse('core:signup')

    def test_signup(self, client):
        """
        Test registration to application
        """

        response: Response = client.post(
            self.url,
            data={
                'username': 'test_username',
                'password': 'test_password',
                'password_repeat': 'test_password',
            },
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['username'] == 'test_username'
