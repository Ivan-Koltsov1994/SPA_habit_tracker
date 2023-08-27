from rest_framework import serializers

from habit.models import Habit


class HabitSerializers(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
