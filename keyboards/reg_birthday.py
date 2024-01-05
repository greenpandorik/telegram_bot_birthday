from aiogram import types


async def reg_birth_day():
    buttons_choice = [
        [
            types.InlineKeyboardButton(
                text="Изменить напоминалку", callback_data="reg_birth_edit"),
            types.InlineKeyboardButton(
                text="Создать напоминалка", callback_data="reg_birth_yes"),
        ],
        [
            types.InlineKeyboardButton(
                text="Показать список напоминаний",
                callback_data="list_birthday")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=buttons_choice, row_width=1)
    return keyboard


async def keyboards_remember_date():
    buttons_choice = [
        [
            types.InlineKeyboardButton(
                text="День в день", callback_data="remember_day_in_day"),
        ],
        [
            types.InlineKeyboardButton(
                text="За 1 день", callback_data="remember_one_day"),
            types.InlineKeyboardButton(
                text="За 2 день", callback_data="remember_two_day")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons_choice,
                                          row_width=1)
    return keyboard


async def keyboards_esit_birthday():
    buttons_choice = [
        [
            types.InlineKeyboardButton(
                text="ФИО/Прозвище", callback_data="edit_name"),
            types.InlineKeyboardButton(
                text="Дата Дня Рождения", callback_data="edit_date"),
        ],
        [
            types.InlineKeyboardButton(
                text="Дата напоминания о Дне Рождении",
                callback_data="edit_remember_date")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons_choice)
    return keyboard


async def keyboards_yes_no():
    buttons_choice = [
        [
            types.InlineKeyboardButton(
                text="Да", callback_data="yes_save"),
            types.InlineKeyboardButton(
                text="Нет", callback_data="no_save"),
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons_choice)
    return keyboard
