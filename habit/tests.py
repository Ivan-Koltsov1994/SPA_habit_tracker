from django.test import TestCase

from django.urls import reverse
from habit.models import Habit
from users.models import User, UserRoles
from rest_framework.test import APITestCase
from rest_framework import status

from users.tests import SetupTestCase
from habit.serializers import HabitSerializers

class HabitsTestCase(APITestCase):
    """Тесты модели Habit"""
    def setUp(self) -> None:
        """Подготовка данных перед каждым тестом"""

        self.user = User(
            email='test@test.ru',
            is_staff=False,
            is_superuser=False,
            is_active=True,
            role=UserRoles.MEMBER,
            chat_id=378037756
                         )
        self.user.set_password('123QWE456RTY')
        self.user.save()
        response = self.client.post(
            '/token/',
            {"email": "test@test.ru",
             "password": "123QWE456RTY",
             "phone": "+79969190940"
             }
        )
        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.test_model_name = 'habit_for_test'

    def test_habit_create(self):
        """Тест создания модели Habit"""
        habit_test = Habit.objects.create(name=self.test_model_name, place="home", time="17:53",
                                          action="pump up the press test",
                                          is_pleasurable=True, periodic=1, reward=None, execution_time="00:02",
                                          is_public=True, owner=self.user, associated_habit=None)

        response = self.client.post('/app/habits/', {'name': "test2", "place": "home", "time": "17:53",
                                                     "action": "pump up the press test", "is_pleasurable": True,
                                                     "periodic": 1, "reward": 'prise', "execution_time": "00:02",
                                                     "is_public": True, "owner": 1})
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(habit_test.name, 'habit_for_test')
        self.assertEqual(response.json(), {'id': 2, 'name': 'test2', 'place': 'home', 'time': '17:53:00',
                                           'action': 'pump up the press test', 'is_pleasurable': True, 'periodic': 1,
                                           'reward': 'prise', 'execution_time': '00:02:00', 'is_public': True, 'owner': 1,
                                           'associated_habit': None})
    def test_list_habits(self):
        """Тест списка модели Habit"""
        Habit.objects.create(name=self.test_model_name, place="home", time="17:53",
                                          action="pump up the press test",
                                          is_pleasurable=True, periodic=1, reward=None, execution_time="00:02",
                                          is_public=True, owner=self.user, associated_habit=None)
        response = self.client.get('/app/habits/')
        # print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.all().count(), 1)
