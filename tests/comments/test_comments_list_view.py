import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response


class TestCommentsListView:
    url = reverse('goals:comment-list')

    @pytest.mark.django_db()
    def test_auth_required_list_view(self, client):
        """
        Unauthorized user get Authorization error
        """
        response: Response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
