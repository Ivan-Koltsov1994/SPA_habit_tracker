from django.core.management import BaseCommand
from users.models import User, UserRoles


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Coздаем обычного пользователя"""
        user = User.objects.create(
            email='user@skypro.com',
            is_staff=False,
            is_superuser=False,
            is_active=True,
            role=UserRoles.MEMBER,
        )
        user.set_password('qwerty123')
        user.save()
        """Coздаем модератора"""
        moderator = User.objects.create(
            email='moder@skypro.com',
            is_staff=True,
            is_superuser=False,
            is_active=True,
            role=UserRoles.MODERATOR,
        )
        moderator.set_password('qwerty123')
        moderator.save()
