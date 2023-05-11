import requests
from django.conf import settings
from requests import Response

from bot.tg.schemas import GetUpdatesResponse, SendMessageResponse


class TgClient:
    """
    Class with telegram bot interactions
    """

    def __init__(self, token: str = settings.BOT_TOKEN) -> None:
        self.token = token

    def get_url(self, method: str) -> str:
        """
        Get url in dependence on method
        :param method: telegram method
        :return: url for request
        """
        return f'https://api.telegram.org/bot{self.token}/{method}'

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        """
        Get updates from telegram bot
        :param offset: offset
        :param timeout: timeout
        :return: response
        """
        response: Response = requests.get(
            self.get_url('getUpdates'), params={'offset': offset, 'timeout': timeout}
        )
        data = response.json()
        return GetUpdatesResponse(**data)

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        """
        Send message to telegram bot
        :param chat_id: chat id
        :param text: text message
        :return: response
        """
        response: Response = requests.get(
            self.get_url('sendMessage'), params={'chat_id': chat_id, 'text': text}
        )
        data = response.json()
        return SendMessageResponse(**data)
