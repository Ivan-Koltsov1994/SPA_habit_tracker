import os
import django
from django.urls import reverse
from rest_framework import status

from users.serializers import UsersSerializers
from rest_framework.test import APITestCase
from users.models import User

django.setup()

class SetupTestCase(APITestCase):
    def setUp(self):
        self.user = User(email='test@test.ru', is_superuser=True, is_staff=True, is_active=True)
        self.user.set_password('123QWE456RTY')
        self.user.save()

        response = self.client.post(
            '/token/',
            {"email": "test@test.ru",
             "password": "123QWE456RTY",
             "phone": "+79969190940",
        }
        )

        self.access_token = response.json().get('access')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

class UserAPITestCase(SetupTestCase):

    def test_list_users(self):
        """Тестируем вывод списка пользователей"""
        response = self.client.get(reverse('users:users_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        """Тестируем создание пользователей"""
        data = {
            "email": "test2@example.com",
            "password": "secret123",
            "phone": "+79969190940"
        }
        response = self.client.post(reverse('users:user_create'), data)
        # print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.last().email, 'test2@example.com')

    def test_retrieve_user(self):
        """Тестируем предосталение информации опользователе"""
        response = self.client.get(reverse('users:users_detail', args=[self.user.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        """Тестируем обновление пользователей"""
        data = {
            "email": "test@example.com",
            "password": "secret123",
            "phone": "+79969190940"
        }
        response = self.client.patch(reverse('users:user_update', args=[self.user.id]), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'test@example.com')

    def test_user_serializer(self):
        """Проверяем работу сериализатора"""
        user = User.objects.create(email='test2@test.ru')
        data = UsersSerializers(user).data

        self.assertEqual(set(data.keys()), {'id', 'email','role','phone', 'city'})

    def test_unauthenticated_user_access(self):
        """Тестируем представление листа пользователей"""
        response = self.client.get(reverse('users:users_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_str(self):
        """Тестируем пользовательское представление создания пользователя"""
        user = User.objects.create(email='test2@test.ru')
        self.assertEqual(str(user), 'test2@test.ru - None: None')
