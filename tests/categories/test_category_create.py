import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from goals.models import GoalCategory
from tests.factories import BoardFactory


@pytest.mark.django_db()
class TestCategoryCreate:
    url = reverse('goals:category-create')

    def test_auth_required(self, client, category_create_data):
        """
        Unauthorized user get Authorization error
        """
        response: Response = client.post(self.url, data=category_create_data())
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_failed_to_create_deleted_category(self, auth_client, user):
        """Can`t create deleted category"""
        board = BoardFactory.create(with_owner=user)
        response = auth_client.post(
            self.url, data={'title': 'test_title', 'board': board.id, 'user': user.id}
        )

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['is_deleted'] is False
        assert GoalCategory.objects.last().is_deleted is False
