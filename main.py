import os
import asyncio
import logging
import sqlite3
import threading
import datetime
import aioschedule

from pathlib import Path
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.state import StatesGroup, State
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from handlers import reg_birthday_answers

load_dotenv()
secret_token = os.getenv('TELEGRAM_TOKEN_BOT')
api_key_yagpt = os.getenv('API_KEY_YAGPT')
bot = Bot(token=secret_token)
path_db = Path("db", "database.db")
conn = sqlite3.connect(path_db, check_same_thread=False)
cursor = conn.cursor()
logging.basicConfig(level=logging.INFO)


class Form_reg(StatesGroup):
    name = State()
    date = State()
    remember_date = State()


class Form_edit(StatesGroup):
    name = State()
    new_name = State()
    date = State()
    remember_date = State()


async def send_message_user(bot: Bot):
    print('HELLO')
    today = (datetime.date.today()).strftime("%d-%m")
    cursor.execute(
        "SELECT name type FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for name_table in tables:
        user_id = int((name_table[0]).split("_")[1])
        cursor.execute(f'SELECT * FROM {name_table[0]} WHERE remember_date=="{today}";')
        birthdays = cursor.fetchall()
        await bot.send_message(user_id, str(birthdays))

# async def send_message_user():
#     print('HELLO')
# def schedule_jobs(dp):
#     # scheduler.add_job(send_message_user, 'cron', hour=23, minute=3)
#     scheduler.add_job(send_message_user, "interval", seconds=5, args=(dp,))




    # Для каждого дня рождения в списке:
    # for name, date, sent in birthdays:
    #     # Получить имя пользователя, которому необходимо отправить напоминание.
    #     user_id = int(date.split("_")[0])
    #     # Отправить пользователю напоминание.
    #     bot.send_message(user_id, f"С днём рождения, {name}!")
    #     # Обновить базу данных, чтобы отметить, что напоминание было отправлено.
    #     cursor.execute("UPDATE birthdays SET sent = 1 WHERE id = ?", (user_id,))
    #     conn.commit()


async def main():
    # Диспетчер
    dp = Dispatcher()
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(
        send_message_user, trigger="interval", seconds=600, kwargs={'bot': bot})
    scheduler.start()
    dp.include_routers(reg_birthday_answers.router)
    # scheduler.add_job(send_message_user, trigger='cron', hour=11, minute=46, start_date=datetime.datetime.now(), kwargs={'bot': bot})
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    # scheduler.start()
    asyncio.run(main())
