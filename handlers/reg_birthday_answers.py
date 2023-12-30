from datetime import datetime as dt
from datetime import timedelta
from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from main import Form
from keyboards.reg_birthday import reg_birth_day, keyboards_remember_date
from utills.request_apigpt import get_msg_yagpt
from utills.check_date import check_format_date, subtract_date
from utills.message import (start_message, reg_message,
                            reg_birth_yes, reg_birth_date_error,
                            reg_birth_date, help_message,
                            reg_date_remember
                            )

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        start_message
    )
    await message.answer(
        reg_message,
        reply_markup=await reg_birth_day()
    )


@router.message(Command("reg"))
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


@router.message(Form.name)
async def save_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    name = await state.get_data()
    await message.answer(reg_birth_date.format(name=name['name']))
    await state.set_state(Form.date)
    # name = await state.get_data()
    # birth_msg = await get_msg_yagpt(name['name'])
    # if birth_msg:
    #     await message.answer(birth_msg)
    # else:
    #     await message.answer(birth_msg_error)


@router.message(Form.date)
async def save_name(message: types.Message, state: FSMContext):
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
    # await state.clear()


@router.callback_query(F.data == "reg_birth_yes")
async def send_random_value(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(reg_birth_yes)
    await state.set_state(Form.name)


@router.callback_query(F.data == "reg_birth_edit")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer()


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
    await callback.message.answer(str(await state.get_data()))
