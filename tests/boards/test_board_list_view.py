import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from goals.serializers import BoardCreateSerializer
from tests.factories import BoardFactory


class TestBoardListView:
    url = reverse('goals:board-list')

    @pytest.mark.django_db()
    def test_auth_required_list_view(self, client):
        """
        Unauthorized user get Authorization error
        """
        response: Response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db()
    def test_auth_list_view(self, auth_client, board_factory: BoardFactory, user):
        """
        Authorized user get boards
        """
        boards = board_factory.create_batch(size=2, with_owner=user)
        response: Response = auth_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data == sorted(
            BoardCreateSerializer(boards, many=True).data, key=lambda x: x['title']
        )
