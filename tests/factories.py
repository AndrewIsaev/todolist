import factory
from django.utils import timezone
from pytest_factoryboy import register

from core.models import User
from goals.models import Board, BoardParticipant, GoalCategory


@register
class UserFactory(factory.django.DjangoModelFactory):
    """User factory"""

    username = factory.Faker('user_name')
    password = factory.Faker('password')

    class Meta:
        model = User

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        return cls._get_manager(model_class).create_user(*args, **kwargs)


class DatesFactory(factory.django.DjangoModelFactory):
    created = factory.LazyFunction(timezone.now)
    updated = factory.LazyFunction(timezone.now)

    class Meta:
        abstract = True


@register()
class BoardFactory(DatesFactory):
    """Board factory"""

    title = factory.Faker('sentence')

    class Meta:
        model = Board

    @factory.post_generation
    def with_owner(self, create, owner, **kwargs):
        if owner:
            BoardParticipant.objects.create(
                board=self, user=owner, role=BoardParticipant.Role.owner
            )


@register()
class BoardParticipantFactory(DatesFactory):
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = BoardParticipant


@register()
class CategoryFactory(DatesFactory):
    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)
    title = factory.Faker('sentence')

    class Meta:
        model = GoalCategory
