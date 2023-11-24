import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from datetime import datetime

from api.api import Dispatcher_DSTU

from threading import Thread

logging.basicConfig(level=logging.INFO)
bot = Bot("TOKIN")
dp = Dispatcher()

disp = Dispatcher_DSTU()

group_id = None
users = {}


async def auto_sending(_day, day):
    for key, value in users.items():
        if value['auto_sending'] == 'off' or None:
            pass
        elif value['auto_sending'] == 'on':
            await bot.send_message(chat_id=key, text=_schedule(key, _day, day))


async def schedule_auto_sending():
    while True:
        now = datetime.now()

        if now.weekday() == 6 and now.hour == 20 and now.minute == 0:
            await auto_sending('monday', "Понедельник")
        if now.weekday() == 0 and now.hour == 20 and now.minute == 0:
            await auto_sending('tuesday', "Вторник")
        if now.weekday() == 1 and now.hour == 20 and now.minute == 0:
            await auto_sending('wednesday', "Среда")
        if now.weekday() == 2 and now.hour == 20 and now.minute == 0:
            await auto_sending('thursday', "Четверг")
        if now.weekday() == 3 and now.hour == 20 and now.minute == 0:
            await auto_sending('friday', "Пятница")
        if now.weekday() == 4 and now.hour == 20 and now.minute == 0:
            await auto_sending('saturday', "Суббота")
            print("!!!")

        await asyncio.sleep(10)
        print("!!")


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
    users[callback.from_user.id] = {'group_id': group_id, 'auto_sending': None}
    await callback.message.edit_text(f'Для того, чтобы изменить группу повторно используйте каманду /start. '
                                     f'Сейчас у вас выбрана группа {disp._find_group(group_id).name}')

    buttons = [
        [
            types.InlineKeyboardButton(text="да", callback_data="auto_sending_on"),
            types.InlineKeyboardButton(text="нет", callback_data="auto_sending_off")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    await callback.message.answer("Хотите включить автоматическую рассылку расписания?", reply_markup=keyboard)


@dp.callback_query(F.data.startswith("auto_sending_"))
async def callbacks_groups(callback: types.CallbackQuery):
    if callback.data.split("_")[2] == "on":
        users[callback.from_user.id]['auto_sending'] = 'on'
        await callback.message.edit_text("Рассылка успешно включина")
    elif callback.data.split("_")[2] == "off":
        users[callback.from_user.id]['auto_sending'] = 'off'
        await callback.message.edit_text("Рассылка успешно выключина")


def _schedule(user_id, _weekday, weekday):
    try:
        if users[user_id]['group_id'] is not None:
            return disp.find_group_schedule_by_day(users[user_id]['group_id'], _weekday, weekday)
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


def start_bot():
    asyncio.run(main())


def start_schedule_auto_sending():
    asyncio.run(schedule_auto_sending())


if __name__ == "__main__":
    thread1 = Thread(target=start_bot)
    thread2 = Thread(target=start_schedule_auto_sending)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()