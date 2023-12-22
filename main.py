import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from handlers import reg_birthday_answers


load_dotenv()
secret_token = os.getenv('TELEGRAM_TOKEN_BOT')
bot = Bot(token=secret_token)
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


# Объект бота
async def main():
    # Диспетчер
    dp = Dispatcher()

    dp.include_routers(reg_birthday_answers.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
