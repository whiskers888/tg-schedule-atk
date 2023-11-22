import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from api.api import Dispatcher_DSTU

logging.basicConfig(level=logging.INFO)
bot = Bot("1068856809:AAE73f6oMnlgzqBMnEkOA0ck65s575119gQ")
dp = Dispatcher()

disp = Dispatcher_DSTU()

group_id = None
user = {}


@dp.message(Command("start"))
async def message_start(message: types.Message):
    buttons = [
        [
            types.InlineKeyboardButton(text="1 курс", callback_data="course_k1"),
            types.InlineKeyboardButton(text="2 курс", callback_data="course_k2")
        ],
        [
            types.InlineKeyboardButton(text="3 курс", callback_data="course_k3"),
            types.InlineKeyboardButton(text="4 курс", callback_data="course_k4")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer(f'Добро пожаловать {message.from_user.first_name}! Выберите свой курс',
                         reply_markup=keyboard)


@dp.callback_query(F.data.startswith("course_"))
async def callbacks_course(callback: types.CallbackQuery):
    if callback.data.split("_")[1] == "k1":
        course = 1
    elif callback.data.split("_")[1] == "k2":
        course = 2
    elif callback.data.split("_")[1] == "k3":
        course = 3
    elif callback.data.split("_")[1] == "k4":
        course = 4

    groups = disp.find_groups_by_course(course)

    keyboard = InlineKeyboardBuilder()
    for group in groups:
        keyboard.add(types.InlineKeyboardButton(text=f"{group.name}", callback_data=f"group_{group.id}"))
    keyboard.adjust(2)

    await callback.message.edit_text('Выберите свою группу', reply_markup=keyboard.as_markup())
    await callback.answer()


@dp.callback_query(F.data.startswith("group_"))
async def callbacks_groups(callback: types.CallbackQuery):
    global group_id
    group_id = int(callback.data.split("_")[1])
    user[callback.from_user.id] = group_id
    await callback.message.edit_text(f'Для того, чтобы изменить группу повторно используйте каманду /start. '
                                     f'Сейчас у вас выбрана группа {disp._find_group(group_id).name}')


def _schedule(user_id, _weekday, weekday):
    try:
        if user[user_id] is not None:
            return disp.find_group_schedule_by_day(user[user_id], _weekday, weekday)
    except KeyError:
        return ("Сначала пожалуйста выберете группу, "
                "для этого используйте комманду /start")


@dp.message(Command('monday'))
async def monday(message: types.Message):
    await message.answer(_schedule(message.from_user.id, "Monday", "Понедельник"))


@dp.message(Command('tuesday'))
async def monday(message: types.Message):
    await message.answer(_schedule(message.from_user.id, "Tuesday", "Вторник"))


@dp.message(Command('wednesday'))
async def monday(message: types.Message):
    await message.answer(_schedule(message.from_user.id, "Wednesday", "Среда"))


@dp.message(Command('thursday'))
async def monday(message: types.Message):
    await message.answer(_schedule(message.from_user.id, "Thursday", "Четверг"))


@dp.message(Command('friday'))
async def monday(message: types.Message):
    await message.answer(_schedule(message.from_user.id, "Friday", "Пятница"))


@dp.message(Command('saturday'))
async def monday(message: types.Message):
    await message.answer(_schedule(message.from_user.id, "Saturday", "Суббота"))


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())