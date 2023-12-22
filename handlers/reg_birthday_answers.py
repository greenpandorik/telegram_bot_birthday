import asyncio
import logging
from aiogram import Router, types, F
from aiogram.filters.command import Command
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


from keyboards.reg_birthday import reg_birth_day

router = Router()


class RegUserBD(StatesGroup):
    name = State()


@router.message(Command("reg"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Ты хочешь добавить День Рождение человека из этого чата?",
        reply_markup=await reg_birth_day()
    )
    # message.chat.id так можно получить id чата для создания таблицы в бд


async def reg_user_bd(message: types.Message):
    await message.answer('Напиши ФИО или прозвище\nЧей день рождения мы записываем')
    print(message)


@router.callback_query(F.data == "add_from_chat")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer('Окей добавляем из чатика')
    await reg_user_bd(callback.message)


@router.callback_query(F.data == "add_from_other")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer('Окей добавляем не из чатика')
