import db
import requests
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import ADMIN_PASS

admin_router = Router()


class Admins(StatesGroup):
    password = State()
    deleted_pos = State()


@admin_router.message(Command("admin"))
async def get_admin(message: Message, state: FSMContext):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="Удалить очередь",
        callback_data="delete charge"
    ))
    builder.row(InlineKeyboardButton(
        text="Удалить человека из очереди",
        callback_data="delete_user"
    ))
    if await requests.check_role(message.from_user.id, "admin"):
        await message.answer("Добро пожаловать в меню для администраторов!", reply_markup=builder.as_markup())
    else:

        await state.set_state(Admins.password)
        await message.answer("Вы хотите стать админом бота?\nТогда введите специальный пароль, для того, чтобы стать админом")


@admin_router.message(Admins.password)
async def set_admin(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()
    if data["password"] == ADMIN_PASS:
        await message.answer("Поздравляем, теперь вы администратор!")
        await requests.set_role(message.from_user.id, "admin")

    else:
        await message.answer("Пароль неправильный")


@admin_router.callback_query(F.data == "delete charge")
async def delete_charge(callback: CallbackQuery):
    await requests.clear_charge()
    await callback.message.answer("Очередь успешно удалена!")


@admin_router.callback_query(F.data == "delete_user")
async def delete_user(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Admins.deleted_pos)
    await callback.message.answer("Введите номер, который Вы хотите удалить")


@admin_router.message(Admins.deleted_pos)
async def delete_user2(message: Message, state: FSMContext):
    await state.update_data(deleted_pos=message.text)
    data = await state.get_data()
    user = await requests.get_user(data["deleted_pos"])
    await requests.delete_user_by_position(data["deleted_pos"])
    await message.answer(f"Пользователь {user.first_name} успешно удален ")

