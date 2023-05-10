from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.schemas import Message
from goals.models import Goal


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tg_client = TgClient()

    def handle(self, *args, **options):
        offset = 0
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                self.handle_message(item.message)

    def handle_message(self, message: Message):
        tg_user, created = TgUser.objects.get_or_create(chat_id=message.chat.id)

        if tg_user.user:
            self.handler_authorized_user(tg_user, message)
        else:
            self.handler_unauthorized_user(tg_user, message)

    def handler_authorized_user(self, tg_user: TgUser, message: Message):
        if message.text == '/goals':
            query_set = (
                Goal.objects.select_related('user')
                .filter(category__is_deleted=False)
                .exclude(status=Goal.Status.archived)
            )
            goals = [f'{goal.id} {goal.title}' for goal in query_set]
            if not goals:
                text = 'No goals'
            else:
                text = '\n'.join(goals)

            self.tg_client.send_message(chat_id=message.chat.id, text=text)

    def handler_unauthorized_user(self, tg_user: TgUser, message: Message):
        verification_code = tg_user.generate_verification_code()
        tg_user.verification_code = verification_code
        tg_user.save()

        self.tg_client.send_message(
            chat_id=message.chat.id,
            text=f'Your verification code is {tg_user.verification_code}',
        )
