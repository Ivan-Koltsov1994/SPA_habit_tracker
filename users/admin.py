from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email','place', 'phone', 'is_active',)
    list_filter = ('id','is_active',)

