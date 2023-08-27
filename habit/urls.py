from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import *

router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habits')


urlpatterns = [
    path('public_habits/', HabitsListView.as_view(), name='habits_list'),
              ] + router.urls
