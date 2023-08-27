from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated

from habit.models import Habit
from habit.permissions import UserPermissionsModerator, UserPermissionsOwner
from habit.serializers import HabitSerializers
from users.models import UserRoles
from habit.tasks import send_telegram_message

# Create your views here.
class HabitViewSet(viewsets.ModelViewSet):
    """Вывод списка всех привычек"""
    serializer_class = HabitSerializers
    queryset = Habit.objects.all()
    # permission_classes = [UserPermissionsModerator,UserPermissionsOwner]

    def get_queryset(self):
        """Фильтруем список привычек только для владельца или модератора"""
        user = self.request.user
        if user.is_staff or user.is_superuser or user.role == UserRoles.MODERATOR:
            return Habit.objects.all()
        else:
            return Habit.objects.filter(owner=user)

    def perform_create(self, serializer) -> None:
        """Сохраняет новому объекту владельца и создает задачу"""
        serializer.save(owner=self.request.user)
        send_telegram_message.delay()

class HabitsListView(generics.ListAPIView):
    """Вывод списка  публичных привычек"""
    serializer_class = HabitSerializers
    queryset = Habit.objects.all()
    # permission_classes = [UserPermissionsModerator,UserPermissionsOwner]


    def get_queryset(self):
        """Фильтруем список привычек только для владельца или модератора"""
        user = self.request.user
        if user.is_staff or user.is_superuser or user.role == UserRoles.MODERATOR:
            return Habit.objects.all()
        else:
            return Habit.objects.filter(public=True)