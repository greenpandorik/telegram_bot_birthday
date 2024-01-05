from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from main import Form_reg, Form_edit
from keyboards.reg_birthday import (keyboards_esit_birthday, reg_birth_day,
                                    keyboards_remember_date, keyboards_yes_no
                                    )
from utills.request_apigpt import get_msg_yagpt
from utills.check_date import check_format_date, subtract_date
from utills.message import (start_message, reg_message,
                            reg_birth_yes, reg_birth_date_error,
                            reg_birth_date, help_message,
                            reg_date_remember, answer_about_add,
                            reg_birth_edit, what_edit_questaion,
                            what_edit_questaion_error, list_remembers,
                            edit_name, edit_remember_date
                            )
from utills.work_with_db import (add_new_remember, check_table_userid,
                                 check_edit_birthday, get_all_birthday,
                                 edit_info_birthday
                                 )

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    # работаем с бд
    await check_table_userid(message.chat.id)
    await message.answer(
        start_message
    )
    await message.answer(
        reg_message,
        reply_markup=await reg_birth_day()
    )


@router.message(Command("menu"))
async def cmd_start(message: types.Message):
    await message.answer(
        reg_message,
        reply_markup=await reg_birth_day()
    )
    # message.chat.id так можно получить id чата для создания таблицы в бд


@router.message(Command("help"))
async def cmd_start(message: types.Message):
    await message.answer(
        help_message
    )


@router.message(Form_reg.name)
async def save_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    name = await state.get_data()
    await message.answer(reg_birth_date.format(name=name['name']))
    await state.set_state(Form_reg.date)
    # name = await state.get_data()
    # birth_msg = await get_msg_yagpt(name['name'])
    # if birth_msg:
    #     await message.answer(birth_msg)
    # else:
    #     await message.answer(birth_msg_error)


@router.message(Form_reg.date)
async def save_date(message: types.Message, state: FSMContext):
    date = None
    try:
        date = await check_format_date(message.text)
        if date is None:
            await message.answer(reg_birth_date_error)
            return
    except BaseException:
        await message.answer(reg_birth_date_error)
        return
    await state.update_data(date=date)
    await message.answer(
        reg_date_remember,
        reply_markup=await keyboards_remember_date()
    )


@router.message(Form_edit.name)
async def save_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    name = (await state.get_data())['name']
    check_name = await check_edit_birthday(name, message.chat.id)
    if check_name:
        rows = await get_all_birthday(message.chat.id, name=name)
        text = ''
        for row in rows:
            text += list_remembers.format(row0=row[0], row1=row[1], row2=row[2])
        await message.answer(
            what_edit_questaion + text,
            reply_markup=await keyboards_esit_birthday()
            )
    else:
        await message.answer(
            what_edit_questaion_error.format(name=name)
            )


@router.message(Form_edit.new_name)
async def save_new_name(message: types.Message, state: FSMContext):
    await state.update_data(new_name=message.text)
    info = await state.get_data()
    await message.answer(
        'Оставляем такой вариант?\n\n' + list_remembers.format(
            row0=info['new_name'],
            row1=info['date'],
            row2=info['remember_date']
            ), reply_markup=await keyboards_yes_no())


@router.message(Form_edit.date)
async def save_new_date(message: types.Message, state: FSMContext):
    date = None
    try:
        date = await check_format_date(message.text)
        if date is None:
            await message.answer(reg_birth_date_error)
            return
    except BaseException:
        await message.answer(reg_birth_date_error)
        return
    await state.update_data(date=date)
    info = await state.get_data()
    await message.answer(
        'Оставляем такой вариант?\n\n' + list_remembers.format(
            row0=info['name'],
            row1=info['date'],
            row2=info['remember_date']
            ), reply_markup=await keyboards_yes_no())


# @router.message(Form_edit.remember_date)
# async def save_new_remember_date(message: types.Message, state: FSMContext):
#     await state.update_data(remember_date=message.text)
#     info = await state.get_data()
#     await message.answer(
#         'Оставляем такой вариант?\n\n' + list_remembers.format(
#             row0=info['name'],
#             row1=info['date'],
#             row2=info['remember_date']
#             ), reply_markup=await keyboards_yes_no())


@router.callback_query(F.data == "yes_save")
async def send_random_value(callback: types.CallbackQuery, state: FSMContext):
    info = await state.get_data()
    try:
        edit = await edit_info_birthday(
            callback.message.chat.id,
            old_name=info['name'],
            new_name=info['new_name'],
            date=info['date'],
            remember_date=info['remember_date']
            )
    except BaseException:
        edit = await edit_info_birthday(
            callback.message.chat.id,
            old_name=info['name'],
            date=info['date'],
            remember_date=info['remember_date']
            )
    if edit:
        await callback.message.edit_text(
            'Данные успешно обновлены!\n\n' + reg_message,
            reply_markup=await reg_birth_day()
        )
    else:
        await callback.message.edit_text('Упс, что то пошло не так....')
    await state.clear()


@router.callback_query(F.data == "no_save")
async def send_random_value(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        reg_message,
        reply_markup=await reg_birth_day()
    )


@router.callback_query(F.data == "reg_birth_yes")
async def send_random_value(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(reg_birth_yes)
    await state.set_state(Form_reg.name)


@router.callback_query(F.data == "reg_birth_edit")
async def send_random_value(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(reg_birth_edit)
    await state.set_state(Form_edit.name)


@router.callback_query(F.data == "list_birthday")
async def send_random_value(callback: types.CallbackQuery):
    rows = await get_all_birthday(callback.message.chat.id)
    text = ''
    for row in rows:
        text += list_remembers.format(row0=row[0], row1=row[1], row2=row[2])
    await callback.message.edit_text(text)


@router.callback_query(F.data.startswith("remember_"))
async def send_random_value(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[1]
    date = await state.get_data()
    if action == "day":
        await state.update_data(
            remember_date=await subtract_date(date['date'], 0))
    elif action == "one":
        await state.update_data(
            remember_date=await subtract_date(date['date'], 1))
    elif action == "two":
        await state.update_data(
            remember_date=await subtract_date(date['date'], 2))
    info_state = await state.get_data()
    try:
        await add_new_remember(
            dict(await state.get_data()), callback.message.chat.id)
    except BaseException:
        await edit_info_birthday(
            callback.message.chat.id,
            old_name=info_state['name'],
            date=info_state['date'],
            remember_date=info_state['remember_date']
            )
    info_state = await state.get_data()
    await callback.message.edit_text(
        answer_about_add.format(
            name=info_state['name'],
            date=info_state['date'],
            remember_date=info_state['remember_date'])
    )
    await state.clear()


@router.callback_query(F.data.startswith("edit_"))
async def edit_birthday_info(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[1]
    name = (await state.get_data())['name']
    all_info = await get_all_birthday(callback.message.chat.id,
                                      name=name)
    for info in all_info:
        await state.update_data(
            name=info[0], date=info[1], remember_date=info[2]
        )
    if action == 'name':
        await callback.message.edit_text(edit_name)
        await state.set_state(Form_edit.new_name)
    elif action == 'date':
        await callback.message.edit_text(reg_birth_date.format(name=name))
        await state.set_state(Form_edit.date)
    elif action == 'remember':
        await callback.message.answer(
            reg_date_remember,
            reply_markup=await keyboards_remember_date()
        )


# def send_remember(user_id, remember_info, message=None):
#     message.answer(
#         message_id=user_id,
#         text=remember_info
#     )
