from django.urls import reverse
from rest_framework import status


class TestProfileView:
    url = reverse('core:profile')

    def test_auth_required(self, client):
        """
        Unauthorized user get Authorization error
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
