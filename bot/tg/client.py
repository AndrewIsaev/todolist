import requests
from django.conf import settings

from bot.tg.schemas import GetUpdatesResponse, SendMessageResponse


class TgClient:
    def __init__(self, token: str = settings.BOT_TOKEN):
        self.token = token

    def get_url(self, method: str) -> str:
        return f'https://api.telegram.org/bot{self.token}/{method}'

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        response = requests.get(
            self.get_url('getUpdates'), params={'offset': offset, 'timeout': timeout}
        )
        data = response.json()
        return GetUpdatesResponse(**data)

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        response = requests.get(
            self.get_url('sendMessage'), params={'chat_id': chat_id, 'text': text}
        )
        data = response.json()
        return SendMessageResponse(**data)
