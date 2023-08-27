from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Habit(models.Model):
    """Модель привычки"""
    name = models.CharField(max_length=100, verbose_name='название')
    owner = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='создатель', **NULLABLE)
    place = models.CharField(max_length=100, verbose_name='место')
    time = models.TimeField(verbose_name='время')
    action = models.CharField(max_length=100, verbose_name='действие')
    is_pleasurable = models.BooleanField(default=True, verbose_name='признак полезной привычки')
    associated_habit = models.ForeignKey('self', on_delete=models.SET_NULL, **NULLABLE,
                                         verbose_name='связанная привычка')
    periodic = models.PositiveSmallIntegerField(default=1, verbose_name='периодичность в днях')
    reward = models.CharField(max_length=150, verbose_name='вознаграждение', **NULLABLE)
    execution_time = models.TimeField(verbose_name='время на выполнение', **NULLABLE)
    is_public = models.BooleanField(default=True, verbose_name='признак публичности')


    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'

    def __str__(self):
        return f'{self.owner} будет {self.action} в {self.time} в {self.place}'
