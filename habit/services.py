from django_celery_beat.models import CrontabSchedule, PeriodicTask


def create_habit_schedule(habit):
    """Создание периодичности и задачи на отправку"""
    crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
            minute=habit.time.minute,
            hour=habit.time.hour,
            day_of_month=f'*/{habit.periodic}',
            month_of_year='*',
            day_of_week='*',
        )

    PeriodicTask.objects.create(
        crontab=crontab_schedule,
        # interval=interval,
        name=f'Habit Task - {habit.name}',
        task='habit.tasks.send_telegram_message',
        args=[habit.id],
    )
