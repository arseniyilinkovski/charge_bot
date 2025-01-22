from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton
from aiogram.fsm.state import StatesGroup, State
import requests
from requests import get_positions

router = Router()

users = {}


class Reg(StatesGroup):
    position = State()


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
    await message.answer("Здравствуйте", reply_markup=keyboard)


@router.message(F.text.lower() == "получить список")
async def get_list(message: Message):
    all_categories = await get_positions()
    text = ""
    for position in all_categories:
        print(position.id)
        text += f"{str(position.id)}. <a href='https://t.me/{position.username}'>{str(position.first_name)}</a>\n"
    await message.answer(text, parse_mode="HTML")


@router.message(F.text.lower() == "занять очередь")
async def book_one(message: Message, state: FSMContext):
    await state.set_state(Reg.position)
    await message.answer("Введите ваш номер в очереди: ")


@router.message(Reg.position)
async def book_one_2(message: Message, state: FSMContext):
    await state.update_data(position=message.text)
    data = await state.get_data()

    try:
        int(data["position"])
    except:
        await message.answer("Вы ввели не число")
    if (int(data["position"]) < 1) or int(data["position"]) > 30:
        await message.answer("Вы не можете занять место меньше 1 или больше 30")
    elif not await requests.check_unique_position(data["position"]):
        await message.answer("Это место уже занято")
    elif await requests.set_user(message.from_user.id, message.from_user.first_name, data["position"], message.from_user.username):
        await message.answer("Вы уже есть в очереди")
    else:
        await requests.set_user(message.from_user.id, message.from_user.first_name, data["position"], message.from_user.username)
        await message.answer(f"Ваш номер в очереди: {data['position']}")




