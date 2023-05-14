from typing import Callable

import pytest
from rest_framework.test import APIClient

from tests.factories import BoardParticipantFactory


@pytest.fixture
def board_create_data(faker) -> Callable:
    def _wrapper(**kwargs) -> dict:
        data = {'title': faker.sentence(2)}
        data |= kwargs
        return data

    return _wrapper


@pytest.fixture()
def category_create_data(faker) -> Callable:
    def _wrapper(**kwargs) -> dict:
        board = BoardParticipantFactory.create()
        data = {
            'title': faker.sentence(2),
            'board': board.board.id,
        }
        data |= kwargs
        return data

    return _wrapper


@pytest.fixture()
def client() -> APIClient:
    return APIClient()


@pytest.fixture()
def auth_client(client: APIClient, user) -> APIClient:
    client.force_login(user)
    return client
