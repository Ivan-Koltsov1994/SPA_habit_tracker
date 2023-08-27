from django.contrib import admin

from habit.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner', 'time', 'is_pleasurable', 'reward', 'is_public')
    list_filter = ('name', 'is_public')