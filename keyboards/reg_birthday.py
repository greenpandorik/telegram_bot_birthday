from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def reg_birth_day():
    buttons_choice = [
        [
            types.InlineKeyboardButton(
                text="Изменить напоминалку", callback_data="reg_birth_edit"),
            types.InlineKeyboardButton(
                text="Создать напоминалка", callback_data="reg_birth_yes")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons_choice)
    return keyboard


async def keyboards_remember_date():
    buttons_choice = [
        [
            types.InlineKeyboardButton(
                text="День в день", callback_data="remember_day_in_day"),
            types.InlineKeyboardButton(
                text="За 1 день", callback_data="remember_one_day"),
            types.InlineKeyboardButton(
                text="За 2 день", callback_data="remember_two_day")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons_choice)
    return keyboard
