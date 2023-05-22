import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response

from tests.factories import UserFactory, CategoryFactory, BoardParticipantFactory


@pytest.mark.django_db()
class TestCategoryRetrieveView:
    @staticmethod
    def get_url(category_pk: int) -> str:
        return reverse('goals:category', kwargs={'pk': category_pk})

    @pytest.fixture(autouse=True)
    def setup(self, goal_category):
        self.url = self.get_url(goal_category.id)

    def test_auth_required_retrieve_view(self, client):
        """
        Unauthorized user get Authorization error
        """
        response: Response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_auth_retrieve_view(
        self,
        auth_client,
        user: UserFactory,
        goal_category: CategoryFactory,
        board_participant: BoardParticipantFactory,
    ):
        """
        Authorized user get category
        """

        response: Response = auth_client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
