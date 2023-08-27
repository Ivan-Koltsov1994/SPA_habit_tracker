from datetime import datetime, timedelta

from telebot import TeleBot
from celery import shared_task

from config import settings
from habit.models import Habit


@shared_task
def send_telegram_message():
    """Отправка сообщения через бот TG"""

    bot = TeleBot(settings.TG_BOT_TOKEN)

    time_now = datetime.now()
    start_time = time_now - timedelta(minutes=10)
    habit_data = Habit.objects.filter(time__gte=start_time)

    for habit in habit_data.filter(time__lte=time_now):
        message = f"{habit.user.login_tg},напоминанию вам о выполнении привычки {habit.action} в {habit.time} в {habit.place}"
        bot.send_message(habit.owner.chat_id, message)