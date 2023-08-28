from rest_framework import serializers

from habit.models import Habit
import datetime

class HabitSerializers(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"


    def valedate(self,value):
        """Метод исключает одновременный выбор связанной привычки и указания вознагражденияя"""
        if value.get('associated_habit') and value.get('reward'):
            raise serializers.ValidationError(
                'Исключён одновременный выбор связанной привычки и указания вознаграждения.')
        if value.get('execution_time') > datetime.time(hour=0, minute=2, second=0):
            raise serializers.ValidationError('Время выполнения должно быть не больше 120 секунд.')
        if 'associated_habit' in value and value.get('associated_habit').is_pleasurable:
            raise serializers.ValidationError(
                'В связанные привычки могут попадать только привычки с признаком приятной '
                'привычки.')
        # if 'associated_habit' in value and value.get('associated_habit') or value.get('reward'):
        if value.get('associated_habit') and value.get('reward'):
            raise serializers.ValidationError(
                'У приятной привычки не может быть вознаграждения или связанной привычки.')
        if value.get('periodic') > 7:
            raise serializers.ValidationError('Нельзя выполнять привычку реже, чем 1 раз в 7 дней.')

        return value