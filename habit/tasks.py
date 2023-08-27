from telebot import TeleBot
from celery import shared_task

from config import settings
from habit.models import Habit


@shared_task
def send_telegram_message(habit_id):
    """Отправка сообщения через бот TG"""
    habit = Habit.objects.get(id=habit_id)
    bot = TeleBot(settings.TG_BOT_TOKEN)
    message = f"Напоминание о выполнении привычки {habit.action} в {habit.time} в {habit.place}"
    bot.send_message(habit.owner.chat_id, message)