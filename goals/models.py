from django.db import models

from core.models import User


class GoalCategory(models.Model):
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    title = models.CharField(verbose_name='Название', max_length=255)
    user = models.ForeignKey(User, verbose_name='Автор', on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name='Удалена', default=False)
    created = models.DateTimeField(verbose_name='Дата создания', auto_now=True)
    updated = models.DateTimeField(
        verbose_name='Дата последнего обновления', auto_now_add=True
    )

    def __str__(self) -> str:
        return self.title


class Goal(models.Model):
    class Meta:
        verbose_name = 'Цель'
        verbose_name_plural = 'Цели'

    class Status(models.IntegerChoices):
        to_do = 1, 'К выполнению'
        in_progress = 2, 'В процессе'
        done = 3, 'Выполнено'
        archived = 4, 'Архив'

    class Priority(models.IntegerChoices):
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
    created = models.DateTimeField(verbose_name='Дата создания', auto_now=True)
    updated = models.DateTimeField(
        verbose_name='Дата последнего обновления', auto_now_add=True
    )

    def __str__(self) -> str:
        return self.title


class GoalComment(models.Model):
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    created = models.DateTimeField(verbose_name='Дата создания', auto_now=True)
    updated = models.DateTimeField(
        verbose_name='Дата последнего обновления', auto_now_add=True
    )
    text = models.TextField()
    goal = models.ForeignKey('goals.Goal', on_delete=models.CASCADE)
