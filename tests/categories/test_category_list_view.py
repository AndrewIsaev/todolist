import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from tests.factories import CategoryFactory


class TestCategoryListView:
    url = reverse('goals:category-list')

    @pytest.mark.django_db()
    def test_auth_required_list_view(self, client):
        """
        Unauthorized user get Authorization error
        """
        response: Response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db()
    def test_auth_list_view(self, auth_client, category_factory: CategoryFactory):
        """
        Authorized user get categories
        """

        categories = category_factory.create_batch(size=2)
        response: Response = auth_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
