from django.contrib import admin

from core.models import User


class UserAdmin(admin.ModelAdmin):
    """
    Class with user admin settings
    """

    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('email', 'first_name', 'last_name', 'username')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    exclude = ('password',)
    readonly_fields = ('last_login', 'date_joined')


# Register your models here.
admin.site.register(User, UserAdmin)
