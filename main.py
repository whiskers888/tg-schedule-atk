import asyncio
import logging
import openpyxl

from api.api import Dispatcher_DSTU
from settings import Settings
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder


logging.basicConfig(level=logging.INFO)
bot = Bot("6670335479:AAHYxHgc8SsPAhzJUxHyL9WtWrOZ67GoAyo")
dp = Dispatcher()

settings = Settings()
dstu_api = Dispatcher_DSTU()

schedule = openpyxl.open("schedule.xlsx", read_only=True)

sheet, group = None, None


@dp.message(Command("start"))
async def message_start(message: types.Message):
    buttons = [
        [
            types.InlineKeyboardButton(text="1 курс", callback_data="course_1"),
            types.InlineKeyboardButton(text="2 курс", callback_data="course_2"),
        ],
        [
            types.InlineKeyboardButton(text="3 курс", callback_data="course_3"),
            types.InlineKeyboardButton(text="4 курс", callback_data="course_4"),
        ],
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer(
        f"Добро пожаловать {message.from_user.first_name}! Выберите свой курс",
        reply_markup=keyboard,
    )


@dp.callback_query(F.data.startswith("course_"))
async def callbacks_course(callback: types.CallbackQuery):
    # global sheet, group
    groups = dstu_api.find_groups_by_course(callback.data.split("_")[1])

    # if callback.data.split("_")[1] == "k1":
    #     sheet = schedule.worksheets[0]
    #     groups = 24
    # elif callback.data.split("_")[1] == "k2":
    #     sheet = schedule.worksheets[1]
    #     groups = 20
    # elif callback.data.split("_")[1] == "k3":
    #     sheet = schedule.worksheets[2]
    #     groups = 19
    # elif callback.data.split("_")[1] == "k4":
    #     sheet = schedule.worksheets[3]
    #     groups = 15
    # else:
    #     groups = 3

    keyboard = InlineKeyboardBuilder()

    for group in groups:
        keyboard.add(
            types.InlineKeyboardButton(
                text=f"{group.name}", callback_data=f"group_{group.id}"
            )
        )

    # for row in range(2, groups):
    #     keyboard.add(
    #         types.InlineKeyboardButton(
    #             text=f"{sheet[6][row].value}", callback_data=f"group_{row - 1}"
    #         )
    #     )

    keyboard.adjust(2)
    await callback.message.edit_text(
        "Выберите свою группу", reply_markup=keyboard.as_markup()
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("group_"))
async def callbacks_groups(callback: types.CallbackQuery):
    group_id = int(callback.data.split("_")[1])
    # schedule = dstu_api.find_schedule_by_group(group_id)
    settings.attach_group(group_id)
    # await callback.message.edit_text(schedule)
    # global group
    # group = int(callback.data.split("_")[1]) + 1
    await callback.message.edit_text(
        f"Для того, чтобы изменить группу повторно используйте каманду /start. "
        f"Сейчас у вас выбрана группа {group_id}"
    )


def schedule_(day_name, day):
    if sheet is None:
        return "Пожалуйста сначала выберите группу, для этого нажмите /start"

    message_out = f"{day_name}\n\n"
    i = 1
    for row in range(day[0], day[1]):
        if row % 2 != 0:
            if sheet[row][group].value is None:
                message_out += f"{i}. {sheet[row][group - 1].value}\n\n"
            else:
                message_out += f"{i}. {sheet[row][group].value}\n\n"
            i += 1
    return message_out


@dp.message(Command("time"))
async def message_time(message: types.Message):
    try:
        message_out = "расписание звонков:\n\n"

        i = 1
        for row in range(7, 16):
            if row % 2 != 0:
                message_out += f"{i}. {sheet[row][1].value} \n\n"
                i += 1

        await message.answer(message_out)
    except TypeError:
        await message.answer(
            "Пожалуйста сначала выберите группу, для этого нажмите /start"
        )


@dp.message(Command("monday"))
async def monday(message: types.Message):
    await message.answer(dstu_api.find_group_schedule_by_day(settings.group, "Monday"))
    # await message.answer(schedule_("Понедельник:", [7, 14]))


@dp.message(Command("tuesday"))
async def monday(message: types.Message):
    await message.answer(schedule_("Вторник:", [19, 26]))


@dp.message(Command("wednesday"))
async def monday(message: types.Message):
    await message.answer(schedule_("Среда:", [31, 38]))


@dp.message(Command("thursday"))
async def monday(message: types.Message):
    await message.answer(schedule_("Четверг:", [43, 50]))


@dp.message(Command("friday"))
async def monday(message: types.Message):
    await message.answer(schedule_("Пятница:", [55, 62]))


@dp.message(Command("saturday"))
async def monday(message: types.Message):
    await message.answer(schedule_("Суббота:", [67, 74]))


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
