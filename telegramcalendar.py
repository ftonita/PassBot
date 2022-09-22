from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
import datetime
import calendar


def create_callback_data(action, year, month, day):
    return ";".join([action, str(year), str(month), str(day)])


def separate_callback_data(data):
    return data.split(";")


def create_calendar(year=None, month=None):
    now = datetime.datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month
    data_ignore = create_callback_data("IGNORE", year, month, 0)
    keyboard = []
    # First row - Month and Year
    row = [InlineKeyboardButton(
        calendar.month_name[month] + " " + str(year), callback_data=data_ignore
    )]
    keyboard.append(row)
    # Second row - Week Days
    row = []
    for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
        row.append(InlineKeyboardButton(day, callback_data=data_ignore))
    keyboard.append(row)

    my_calendar = calendar.monthcalendar(year, month)
    for week in my_calendar:
        row = []
        for day in week:
            if day == 0:
                row.append(InlineKeyboardButton(
                    " ", callback_data=data_ignore))
            else:
                row.append(
                    InlineKeyboardButton(
                        str(day),
                        callback_data=create_callback_data(
                            "DAY", year, month, day),
                    )
                )
        keyboard.append(row)
    # Last row - Buttons
    row = [InlineKeyboardButton(
        "<", callback_data=create_callback_data("PREV-MONTH", year, month, day)
    ), InlineKeyboardButton(" ", callback_data=data_ignore), InlineKeyboardButton(
        ">", callback_data=create_callback_data("NEXT-MONTH", year, month, day)
    )]
    keyboard.append(row)

    return InlineKeyboardMarkup(keyboard)


async def process_calendar_selection(bot, callback_query):
    ret_data = (False, None)
    query = callback_query
    (action, year, month, day) = separate_callback_data(query.data)
    curr = datetime.datetime(int(year), int(month), 1)
    if action == "IGNORE":
        await bot.answer_callback_query(callback_query_id=query.id)
    elif action == "DAY":
        await bot.edit_message_text(
            text=query.message.text,
            chat_id=query.from_user.id,
            message_id=query.message.id,
        )
        ret_data = True, datetime.datetime(int(year), int(month), int(day))
    elif action == "PREV-MONTH":
        pre = curr - datetime.timedelta(days=1)
        await bot.edit_message_text(
            text=query.message.text,
            chat_id=query.from_user.id,
            message_id=query.message.id,
            reply_markup=create_calendar(int(pre.year), int(pre.month)),
        )
    elif action == "NEXT-MONTH":
        ne = curr + datetime.timedelta(days=31)
        await bot.edit_message_text(
            text=query.message.text,
            chat_id=query.from_user.id,
            message_id=query.message.id,
            reply_markup=create_calendar(int(ne.year), int(ne.month)),
        )
    else:
        await bot.answer_callback_query(
            callback_query_id=query.id, text="Something went wrong!"
        )
    return ret_data
