import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from goals.models import Board, BoardParticipant


class TestBoardCreate:
    url = reverse('goals:board-create')

    def test_auth_required(self, client, board_create_data):
        """
        Unauthorized user get Authorization error
        """
        response: Response = client.post(self.url, data=board_create_data())
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db()
    def test_failed_to_create_deleted_board(self, auth_client, board_create_data):
        """Can`t create deleted board"""
        response = auth_client.post(self.url, data=board_create_data(is_deleted=True))

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['is_deleted'] is False
        assert Board.objects.last().is_deleted is False

    @pytest.mark.django_db()
    def test_request_user_became_board_owner(
        self, auth_client, board_create_data, user
    ):
        """
        Test user became board owner
        """
        response = auth_client.post(self.url, data=board_create_data())
        board_participant = BoardParticipant.objects.get(user_id=user.id)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] == board_participant.board.id
        assert board_participant.role == BoardParticipant.Role.owner
