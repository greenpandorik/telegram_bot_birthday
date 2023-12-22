from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def reg_birth_day():
    buttons_choice = [
        [
            types.InlineKeyboardButton(
                text="Нет", callback_data="add_from_other"),
            types.InlineKeyboardButton(
                text="Да", callback_data="add_from_chat")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons_choice)
    return keyboard
