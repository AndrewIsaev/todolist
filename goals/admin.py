from django.contrib import admin

from goals.models import GoalCategory, Goal, GoalComment


# Register your models here.


@admin.register(GoalCategory)
class GoalCategoryAdmin(admin.ModelAdmin):
    """
    Goal category admin settings
    """

    list_display = ('title', 'user', 'created', 'updated')
    search_fields = ('title', 'user')


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    """
    Goal admin settings
    """

    list_display = ('title', 'user', 'category', 'due_date', 'status')
    search_fields = ('title', 'user')


@admin.register(GoalComment)
class GoalCommentAdmin(admin.ModelAdmin):
    """
    Goal comment admin settings
    """

    list_display = ('text', 'user', 'goal', 'created', 'updated')
    search_fields = ('text', 'user')
