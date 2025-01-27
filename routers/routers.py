from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
import requests
from config import ADMIN_PASS
from requests import get_positions
from aiogram.exceptions import TelegramBadRequest

router = Router()


class Reg(StatesGroup):
    position = State()
    new_position = State()


@router.message(Command("start"))
async def hello(message: Message):
    kb = [
        [
            KeyboardButton(text="Занять очередь"),
            KeyboardButton(text="Получить список")
        ],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )
    await message.answer("Добрый вечер", reply_markup=keyboard)


@router.message(F.text.lower() == "получить список")
async def get_list(message: Message):
    all_categories = await get_positions()
    text = ""
    for position in all_categories:
        if position.username == "NULL":
            text += f"{str(position.id)}. {str(position.first_name)}\n"
        else:

            text += f"{str(position.id)}. {str(position.first_name)} @{position.username}\n"
    try:

        await message.answer(text, parse_mode="HTML")

    except TelegramBadRequest:
        text = "Очередь пуста"
        await message.answer(text, parse_mode="HTML")


@router.message(F.text.lower() == "занять очередь")
async def book_one(message: Message, state: FSMContext):
    await state.set_state(Reg.position)
    await message.answer("Введите ваш номер в очереди: ")


@router.message(Reg.position)
async def book_one_2(message: Message, state: FSMContext):
    await state.update_data(position=message.text)
    data = await state.get_data()
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="Изменить очередь",
        callback_data="change_position"))
    try:
        int(data["position"])
    except ValueError:
        await message.answer("Ошибка")
        await state.clear()
    if (int(data["position"]) < 1) or int(data["position"]) > 30:
        await message.answer("Вы не можете занять место меньше 1 или больше 30")
        await state.clear()
    elif not await requests.check_unique_position(data["position"]):
        await message.answer("Это место уже занято")
        await state.clear()
    elif await requests.set_user(message.from_user.id, message.from_user.first_name, data["position"], message.from_user.username):
        await message.answer("Вы уже есть в очереди, вы хотите поменять свое место(место меняется на любое свободное)", reply_markup=builder.as_markup())
        await state.clear()
    else:
        await requests.set_user(message.from_user.id, message.from_user.first_name, data["position"], message.from_user.username)
        await message.answer(f"Ваш номер в очереди: {data['position']}")
        await state.clear()


@router.callback_query(F.data == "change_position")
async def change_position(callback: CallbackQuery, state: FSMContext):
    # await requests.delete_user(callback.message.from_user.id)
    await state.set_state(Reg.new_position)
    await callback.message.answer("Введите ваш новый номер")


@router.message(Reg.new_position)
async def put_new_position(message: Message, state: FSMContext):
    await state.update_data(new_position=message.text)
    data = await state.get_data()
    await requests.delete_user(message.from_user.id)
    try:
        int(data["new_position"])
    except ValueError:
        await message.answer("Ошибка")
    if (int(data["new_position"]) < 1) or int(data["new_position"]) > 30:
        await message.answer("Вы не можете занять место меньше 1 или больше 30")
    elif not await requests.check_unique_position(data["new_position"]):
        await message.answer("Это место уже занято")
    else:
        await requests.set_user(message.from_user.id, message.from_user.first_name, data["new_position"],
                                message.from_user.username)
        await message.answer(f"Ваш новый номер в очереди: {data['new_position']}")
        await state.clear()



