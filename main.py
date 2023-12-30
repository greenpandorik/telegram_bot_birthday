import os
import asyncio
import logging

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.fsm.state import StatesGroup, State

from handlers import reg_birthday_answers

load_dotenv()
secret_token = os.getenv('TELEGRAM_TOKEN_BOT')
api_key_yagpt = os.getenv('API_KEY_YAGPT')
bot = Bot(token=secret_token)
logging.basicConfig(level=logging.INFO)


class Form(StatesGroup):
    name = State()
    date = State()
    remember_date = State()


# Объект бота
async def main():
    # Диспетчер
    dp = Dispatcher()

    dp.include_routers(reg_birthday_answers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
