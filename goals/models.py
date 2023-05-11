from django.db import models

from core.models import User


class BaseModel(models.Model):
    """
    Base model with created and updated date
    """

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Board(BaseModel):
    """
    Board model
    """

    class Meta:
        verbose_name = 'Доска'
        verbose_name_plural = 'Доски'

    title = models.CharField(verbose_name='Название', max_length=255)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)


class BoardParticipant(BaseModel):
    """
    Board participant model
    """

    class Meta:
        unique_together = ('board', 'user')
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'

    class Role(models.IntegerChoices):
        """
        Choices of role
        """

        owner = 1, 'Владелец'
        writer = 2, 'Редактор'
        reader = 3, 'Читатель'

    board = models.ForeignKey(
        Board,
        verbose_name='Доска',
        on_delete=models.PROTECT,
        related_name='participants',
    )

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.PROTECT,
        related_name='participants',
    )

    role = models.PositiveSmallIntegerField(
        verbose_name='Роль', choices=Role.choices, default=Role.owner
    )
    editable_choices = Role.choices[1:]


class GoalCategory(BaseModel):
    """
    Coal category model
    """

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    board = models.ForeignKey(
        Board, verbose_name='Доска', on_delete=models.PROTECT, related_name='categories'
    )
    title = models.CharField(verbose_name='Название', max_length=255)
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)

    def __str__(self) -> str:
        return self.title


class Goal(BaseModel):
    """
    Goal model
    """

    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    class Status(models.IntegerChoices):
        """
        Status choices
        """

        to_do = 1, 'К выполнению'
        in_progress = 2, 'В процессе'
        done = 3, 'Выполнено'
        archived = 4, 'Архив'

    class Priority(models.IntegerChoices):
        """
        Priority choices
        """

        low = 1, 'Низкий'
        medium = 2, 'Средний'
        high = 3, 'Высокий'
        critical = 4, 'Критический'

    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        'goals.GoalCategory', on_delete=models.PROTECT, related_name='goals'
    )
    due_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey('core.User', on_delete=models.PROTECT)
    status = models.PositiveSmallIntegerField(
        choices=Status.choices, default=Status.to_do
    )
    priority = models.PositiveSmallIntegerField(
        choices=Priority.choices, default=Priority.medium
    )

    def __str__(self) -> str:
        return self.title


class GoalComment(BaseModel):
    """
    Goal comment model
    """

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    text = models.TextField()
    goal = models.ForeignKey('goals.Goal', on_delete=models.CASCADE)
