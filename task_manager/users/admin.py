from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from task_manager.users.models import HexletUser


class UserInline(admin.StackedInline):
    model = HexletUser
    can_delete = False
    verbose_name_plural = 'hexlet_users'


class UserAdmin(BaseUserAdmin):
    inlines = (UserInline,)


admin.site.register(User, UserAdmin)
