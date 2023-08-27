from django.shortcuts import render
from rest_framework import viewsets

from habit.models import Habit
from habit.serializers import HabitSerializers


# Create your views here.
class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializers
    queryset = Habit.objects.all()
