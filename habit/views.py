from rest_framework import viewsets, generics

from habit.models import Habit
from habit.pagination import HabitPagination
from habit.serializers import HabitSerializers
from habit.services import create_habit_schedule
from users.models import UserRoles


# Create your views here.
class HabitViewSet(viewsets.ModelViewSet):
    """Вывод списка всех привычек"""
    serializer_class = HabitSerializers
    queryset = Habit.objects.all()
    pagination_class = HabitPagination

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
        habit = serializer.save()
        create_habit_schedule(habit)


class HabitsListView(generics.ListAPIView):
    """Вывод списка  публичных привычек"""
    serializer_class = HabitSerializers
    queryset = Habit.objects.all()
    pagination_class = HabitPagination

    # permission_classes = [UserPermissionsModerator,UserPermissionsOwner]

    def get_queryset(self):
        """Фильтруем список привычек только для владельца или модератора"""
        user = self.request.user
        if user.is_staff or user.is_superuser or user.role == UserRoles.MODERATOR:
            return Habit.objects.all()
        else:
            return Habit.objects.filter(is_public=True)
