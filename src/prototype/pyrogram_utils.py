import os
import random
from warnings import catch_warnings
import tgcrypto
import unicodedata
from pyrogram import Client, filters, types
from pyrogram.types import KeyboardButton
import pyqrcode as pq
import telegramcalendar
from classic_utils import *
from mail import *
from mysql_utils import *
from telegramcalendar import *

from config import api_id, api_hash, bot_token
# bot_token = "5761358088:AAGoBiwLt69qRkI439sKdfCz__tCS3jRLNk" test


app = Client("21passbot", api_id=api_id,
             api_hash=api_hash, bot_token=bot_token)

START_CMD = "/start"

HELLO_TXT = "Привет, я - бот Школы 21 для приглашения гостей в школу. Для авторизации напиши свою школьную почту (" \
            "@student.21-school.ru - для студентов, @21-school.ru - для персонала) "

STUD_MAIL_ADDRESS = "@student.21-school.ru"
SCH_MAIL_ADDRESS = "@21-school.ru"


CREATE_PASS_BUTTON = "✅ Создать пропуск"
VIEW_MY_PASS_BUTTON = "📄 Мои пропуски"
GET_ADM = "/ADM"
MAIN_MENU_BTN = "🔙Вернуться на Главную"

ADM_MM = "⭐️ ADM"

NAME_MSG = "Введи ФИО гостя, пожалуйста!"
DOCS_MSG = "Это точно реальный человек? :) Введи номер документа, удостоверяющего личность (паспорт)."
DATE_MSG = "Отлично! Теперь нам нужно знать, когда твой гость планирует посетить школу. Выбери нужную дату"
TIME_MSG = "Почти закончили! Подскажи, во сколько (с 10:00 до 19:00) планирует прийти твой гость? (укажи только " \
           "час, например, 15 будет означать 15:00) "
BYE_MSG = (
    "Суперски! Запрос отправлен. Теперь нужно немножко подождать, пока АДМ его одобрят!"
)

RULE_34 = "Обрати внимание на несколько правил: Гостей можно приводить с 10:00 до 19:00 в будние дни\n1 участник за " \
          "одно посещение может привести не более 2 гостей\nПродолжительность визита - не более 1 часа\nНа территории " \
          "«Школы 21» каждый гость должен быть всегда в сопровождении участника\nНужно заполнить эту гугл-форму не " \
          "позднее, чем за 1 день до визита в рабочее время (пн - пт с 10:00 до 19:00)\nНа входе гостю необходимо " \
          "предъявить паспорт "

LAST_PASSES_LIST = "📒Список последних пропусков"
CHECK_NEW_PASS = "📄 Обработать заявку"
CHECK_PASS = "🔍 Поиск по номеру пропуска"

ACCEPT_BUTTON = "✅ ПРИНЯТЬ"
DECLINE_BUTTON = "❌ ОТКЛОНИТЬ"

main_menu_button = types.KeyboardButton(MAIN_MENU_BTN)

create_pass_button: KeyboardButton = types.KeyboardButton(CREATE_PASS_BUTTON)
my_passes_button = types.KeyboardButton(VIEW_MY_PASS_BUTTON)

adm_button = types.KeyboardButton(ADM_MM)
view_all = types.KeyboardButton(LAST_PASSES_LIST)
get_one = types.KeyboardButton(CHECK_NEW_PASS)
get_one_byID = types.KeyboardButton(CHECK_PASS)

accept_button = types.InlineKeyboardButton(text=ACCEPT_BUTTON, callback_data="['value', '" + ACCEPT_BUTTON + "', '+']")
decline_button = types.InlineKeyboardButton(text=DECLINE_BUTTON, callback_data="['value', '" + DECLINE_BUTTON + "', '+']")

adm_choice_markup = types.InlineKeyboardMarkup([[accept_button],[decline_button]])

markup = types.ReplyKeyboardMarkup(
    keyboard=[[create_pass_button, my_passes_button]], resize_keyboard=True
)

adm_markup = types.ReplyKeyboardMarkup(
    keyboard=[[adm_button], [create_pass_button, my_passes_button]], resize_keyboard=True
)

adm_panel_markup = types.ReplyKeyboardMarkup(
    keyboard=[[view_all], [get_one], [get_one_byID], [main_menu_button]], resize_keyboard=True
)

main_menu_markup = types.ReplyKeyboardMarkup(
    keyboard=[[main_menu_button]], resize_keyboard=True
)

async def admGetPass():
    cursor = cnx.cursor()
    print_log("Database connection successful!")
    try:
        query = "SELECT * FROM `Passes` WHERE `status` = '0' LIMIT 1"
        cursor.execute(query)
        res = cursor.fetchall()
        if len(res) == 0:
            tmp = "📄 Нет необработанных заявок!"
        else:
            for i in res:
                if str(i[6]) == '0':
                    stat = "🔵 В ОБРАБОТКЕ"
                elif str(i[6]) == '1':
                    stat = "🟢 ОДОБРЕН"
                elif str(i[6]) >= '2':
                    stat = "🔴 НЕДЕЙСТВИТЕЛЕН"
                inviter = await getUserState(str(i[1]), 'nickname')
                tmp = (
                    "\nПРОПУСК №"
                    + str(i[0])
                    + "\nАВТОР: "
                    + str(inviter)
                    + "\nИМЯ ГОСТЯ: "
                    + str(i[2])
                    + "\nДОКУМЕНТ: "
                    + str(i[3])
                    + "\nДАТА: "
                    + str(i[4])
                    + "\nВРЕМЯ: "
                    + str(i[5])
                    + ":00\nСТАТУС: "
                    + stat
                )
        print_log("Passes have selected successful or no passes have found!")
    except Exception as ex:
        print_log("[Error] Passes list select error: ")
        print_log(ex)
    cursor.close()
    return tmp

async def getPassesList(user_id, count):
    cursor = cnx.cursor()
    print_log("Database connection successful!")
    try:
        query = "SELECT * FROM `Passes` ORDER BY `pass_id` DESC LIMIT 25"
        cursor.execute(query)
        res = cursor.fetchall()
        tmp = ""
        if len(res) == 0:
            await simpleMessage(app, user_id, "📄 В базе данных нет пропусков!")
        else:
            for i in res:
                inviter_nick = await getUserState(i[1], 'nickname')
                if str(i[6]) == '0':
                    stat = "🔵 "
                elif str(i[6]) == '1':
                    stat = "🟢 "
                elif str(i[6]) >= '2':
                    stat = "🔴 "
                tmp = tmp + f"{stat} №{str(i[0])} | {str(i[4])} {str(i[5])}:00 | [{inviter_nick}](tg://user?id={i[1].strip()})\n"
        print_log("Passes have selected successful or no users have found!")
        await simpleMessage(app, user_id, tmp)
    except Exception as ex:
        print_log("[Error] Passes list select error: ")
        print_log(ex)
    cursor.close()

async def getPassByID(pass_id):
    cursor = cnx.cursor()
    print_log("Database connection successful!")
    try:
        query = "SELECT * FROM `Passes` WHERE `pass_id` = " + str(pass_id)
        cursor.execute(query)
        res = cursor.fetchall()
        if len(res) == 0:
            tmp = "📄 Пропуск не найден!"
        else:
            for i in res:
                if str(i[6]) == '0':
                    stat = "🔵 В ОБРАБОТКЕ"
                elif str(i[6]) == '1':
                    stat = "🟢 ОДОБРЕН"
                elif str(i[6]) == '2':
                    stat = "🔴 НЕДЕЙСТВИТЕЛЕН"
                tmp = (
                    "\nПРОПУСК №"
                    + str(i[0])
                    + "\nИМЯ: "
                    + str(i[2])
                    + "\nДОКУМЕНТ: "
                    + str(i[3])
                    + "\nДАТА: "
                    + str(i[4])
                    + "\nВРЕМЯ: "
                    + str(i[5])
                    + ":00\nСТАТУС: "
                    + stat
                )
        print_log("Passes have selected successful or no passes have found!")
    except Exception as ex:
        print_log("[Error] Passes list select error: ")
        print_log(ex)
    cursor.close()
    return tmp

async def getMyPasses(user_id):
    cursor = cnx.cursor()
    print_log("Database connection successful!")
    try:
        query = "SELECT * FROM `Passes` WHERE `inviter_id` = " + str(user_id) + " AND `status` < '2'"
        cursor.execute(query)
        res = cursor.fetchall()
        if len(res) == 0:
            await simpleMessage(app, user_id, "📄 У тебя нет активных пропусков!")
        else:
            for i in res:
                if str(i[6]) == '0':
                    stat = "🔵 В ОБРАБОТКЕ"
                elif str(i[6]) == '1':
                    stat = "🟢 ОДОБРЕН"
                elif str(i[6]) == '2':
                    stat = "🔴 НЕДЕЙСТВИТЕЛЕН"
                tmp = (
                    "\nПРОПУСК №"
                    + str(i[0])
                    + "\nИМЯ: "
                    + str(i[2])
                    + "\nДОКУМЕНТ: "
                    + str(i[3])
                    + "\nДАТА: "
                    + str(i[4])
                    + "\nВРЕМЯ: "
                    + str(i[5])
                    + ":00\nСТАТУС: "
                    + stat
                )
                try:
                    value = str(i[0])
                except Exception as _ex:
                    print("[Error] ", _ex)
                res = pq.create(value)
                res.png(f'cache/{value}.png', scale=6)
                with open(f'cache/{value}.png', 'rb') as photo:
                    await app.send_media_group(user_id, [types.InputMediaPhoto(photo, caption=tmp)])
                os.system(f'rm -rf cache/{value}.png')
        print_log("Passes have selected successful or no users have found!")
    except Exception as ex:
        print_log("[Error] Passes list select error: ")
        print_log(ex)
    cursor.close()

async def getUserState(user_id, row):
    state = database_select_user_row(user_id, row)
    return state


@app.on_message(filters.all)
async def message_handler(client, message):
    text = ""
    try:
        text = str(message.text)
        if '\\' in text:
            text = ""
    except:
        text = ""
    # ЗДЕСЬ БУДЕТ ПРОВЕРКА НА НАЛИЧИЕ ЮЗЕРА В БД
    role = int(await getUserState(message.from_user.id, "role"))
    state = int(await getUserState(message.from_user.id, "state"))
    user = User()
    user.user_id = message.from_user.id
    if state == -1:
        if text == START_CMD:
            await simpleMessage(app, message.from_user.id, HELLO_TXT)
            user.campus = -1
            user.full_name = ""
            user.role = 1
            database_add_user(user)
            await setUserState(message.from_user.id, "state", 0)
    elif state == 0:
        if (
            STUD_MAIL_ADDRESS in text
            or SCH_MAIL_ADDRESS in text
            and 1 < len(text) < 100
        ):
            print_log(text)
            user.email = text
            user.nickname = text.split("@")[0]
            code = random.randint(100000, 999999)

            print_log("code: " + str(code))
            # отправка сообщения
            print_log(send_email(str(code), user.email))
            # отправка сообщения
            await simpleMessage(
                app,
                message.from_user.id,
                str("Код подтверждения был отправлен на почту " + text + ". Если письмо не пришло, проверь папку 'Спам', а также введенный адрес эл. почты"),
            )
            await setUserState(message.from_user.id, "email", user.email)
            await setUserState(message.from_user.id, "nickname", user.nickname)
            await setUserState(message.from_user.id, "code", code)
            await setUserState(message.from_user.id, "state", 1)
        else:
            await simpleMessage(
                app,
                message.from_user.id,
                "Для авторизации напиши свою школьную почту (пример: ftonita@student.21-school.ru)"
            )
    elif state == 1:
        print("TMP: ", int(await getUserState(message.from_user.id, "code")))
        tmp = str(await getUserState(message.from_user.id, "code"))
        if tmp in text and text != "None":
            await setUserState(message.from_user.id, "state", 2)
            await simpleMessage(app, message.from_user.id, "Авторизация прошла успешно")
            await simpleMessage(
                app, message.from_user.id, "Введи своё имя (желательно ФИО)"
            )
        else:
            await setUserState(message.from_user.id, "state", 0)
            await simpleMessage(
                app,
                message.from_user.id,
                "❌ Неверный код подтверждения! Введи почту еще раз!",
            )
    elif state == 2:
        if 1 < len(text) < 100 and text != "None":
            user.full_name = text
            if await setUserState(message.from_user.id, "full_name", user.full_name) == 2:
                await simpleMessage(app, message.from_user.id, "❌ Требуется ввести своё имя!")
                return 
            await setUserState(message.from_user.id, "state", 3)
            await simpleMessage(
                app, message.from_user.id, "Из какого ты кампуса(напиши: msc/kzn/nsk)?"
            )
        else:
            await simpleMessage(app, message.from_user.id, "❌ Требуется ввести своё имя!")
    elif state == 3:
        if len(text) > 1 and text != "None":
            if "msс" in text.lower():
                user.campus = 1
            elif "kzn" in text.lower():
                user.campus = 2
            elif "nsk" in text.lower():
                user.campus = 3
            else:
                await simpleMessage(
                    app,
                    message.from_user.id,
                    "❌ Некорректный ввод кампуса!\nОбразец: msc/kzn/nsk",
                )
                return
            await setUserState(message.from_user.id, "campus", user.campus)
            await setUserState(message.from_user.id, 'state', 4)
            await app.send_message(
                message.chat.id, "✅ Регистрация прошла успешно!", reply_markup=markup
            )
        else:
            await simpleMessage(
                app,
                message.from_user.id,
                "❌ Некорректный ввод кампуса!\nОбразец: msc/kzn/nsk",
            )
    if 10 > state >= 4:
        #TEXT
        if text == MAIN_MENU_BTN:
            if (state > 4):
                deletePass(message.from_user.id)
            if role == 1:
                await setUserState(message.from_user.id, "state", 4)
                await app.send_message(message.chat.id, "🏠 Главное меню", reply_markup=markup)
            elif role == 2:
                await setUserState(message.from_user.id, "state", 10)
                await app.send_message(message.chat.id, "🏠 Главное меню", reply_markup=adm_markup)
        #USER STATE
        elif state == 4:
            if text == CREATE_PASS_BUTTON:
                await simpleMessage(app, message.from_user.id, RULE_34)
                await setUserState(message.from_user.id, "state", 5)
                await app.send_message(
                    message.from_user.id, NAME_MSG, reply_markup=main_menu_markup
                )
            elif text == VIEW_MY_PASS_BUTTON:
                await simpleMessage(app, message.from_user.id, "📌 Список твоих пропусков 📌")
                await getMyPasses(message.from_user.id)
            else:
                await app.send_message(
                    message.chat.id, "Главное меню", reply_markup=markup
                )
        elif state == 5:
            if 1 < len(text) < 100 and text != "None":
                pass_ = Pass()
                pass_.guest_name = text
                pass_.inviter_id = message.from_user.id
                pass_.campus = int(await getUserState(message.from_user.id, "campus"))
                if database_add_pass(pass_) == 2:
                    await simpleMessage(app, message.from_user.id, "❌ Введи ФИО гостя!")
                    return
                await setUserState(message.from_user.id, "state", 6)
                await simpleMessage(app, message.from_user.id, DOCS_MSG)
            else:
                await simpleMessage(app, message.from_user.id, "❌ Введи ФИО гостя!")
        elif state == 6:
            if 1 < len(text) < 100 and text != "None":
                if setPassRow(message.from_user.id, "doc_number", text) == 2:
                    await simpleMessage(
                    app,
                    message.from_user.id,
                    "Введи настоящий номер документа!\nЕсли документа нет, напиши, кем тебе приходится этот человек ("
                    "брат, сестра, друг и т.д)",
                )
                    return
                await setUserState(message.from_user.id, "state", 7)
                await app.send_message(
                    message.from_user.id,
                    DATE_MSG,
                    reply_markup=telegramcalendar.create_calendar(),
                )
            else:
                await simpleMessage(
                    app,
                    message.from_user.id,
                    "Введи настоящий номер документа!\nЕсли документа нет, напиши, кем тебе приходится этот человек ("
                    "брат, сестра, друг и т.д)",
                )
        elif state == 7:
            await app.send_message(
                message.from_user.id,
                "❌ Выбери дату в календаре выше!",
            )
        elif state == 8:
            if len(text) > 0:
                try:
                    hour = int(text)
                    if 10 <= hour <= 19 and text != "None":
                        setPassRow(message.from_user.id, "hour", hour)
                        setPassRow(message.from_user.id, "state", 1)
                        if role == 1:
                            await setUserState(message.from_user.id, "state", 4)
                            await app.send_message(message.from_user.id, BYE_MSG, reply_markup=markup)
                        elif role == 2:
                            await setUserState(message.from_user.id, "state", 10)
                            await app.send_message(message.from_user.id, BYE_MSG, reply_markup=adm_markup)
                    else:
                        await simpleMessage(
                            app,
                            message.from_user.id,
                            "Напиши корректное время для посещения: с 10 до 19 часов!",
                        )
                except Exception as _ex:
                    await simpleMessage(
                        app,
                        message.from_user.id,
                        "Напиши корректное время для посещения: с 10 до 19 часов!",
                    )
    #ADM STATE
    elif state >= 10:
        if text == MAIN_MENU_BTN:
            deletePass(message.from_user.id)
            await setUserState(message.from_user.id, "state", 10)
            await app.send_message(message.chat.id, "🏠 Главное меню", reply_markup=adm_markup)
        elif state == 10:
            if text == CREATE_PASS_BUTTON:
                await setUserState(message.from_user.id, "state", 5)
                await app.send_message(
                    message.from_user.id, NAME_MSG, reply_markup=main_menu_markup
                )
            elif text == VIEW_MY_PASS_BUTTON:
                await simpleMessage(app, message.from_user.id, "📌 Список твоих пропусков 📌")
                await getMyPasses(message.from_user.id)
            elif text == ADM_MM:
                await app.send_message(message.from_user.id, "⭐️ Панель Администратора", reply_markup=adm_panel_markup)
                await setUserState(message.from_user.id, 'state', 11)
            else:
                await app.send_message(message.chat.id, "🏠 Главное меню", reply_markup=adm_markup)
        elif state == 11:
            if text == LAST_PASSES_LIST:
                await simpleMessage(app, message.from_user.id, "📒 Список последних 25 пропусков:")
                await getPassesList(message.from_user.id, 25)
            elif text == CHECK_NEW_PASS:
                new_pass = await admGetPass()
                await app.send_message(message.from_user.id, new_pass, reply_markup=adm_choice_markup)
            elif text == CHECK_PASS:
                await simpleMessage(app, message.from_user.id, "Введи номер пропуска: ")
                await setUserState(message.from_user.id, 'state', 12)
            else:
                await app.send_message(message.from_user.id, ADM_MM, reply_markup=adm_panel_markup)
        elif state == 13:
            try:
                temp = getPassByID(int(text))
                await simpleMessage(app, message.from_user.id, temp)
                await setUserState(message.from_user.id, 'state', 10)
            except:
                print_log("ERROR")
                await simpleMessage(app, message.from_user.id, "Введи валидный номер пропуска")

        

            
    @app.on_callback_query()
    async def CallBackQueryHandler(client, callback_query):
        try:
            state = int(await getUserState(callback_query.from_user.id, "state"))
            if state == 7:
                selected, date = await telegramcalendar.process_calendar_selection(
                    app, callback_query
                )
                tmp = datetime.datetime.now().date().isoformat()

                if selected:
                    if tmp < str(date.strftime("%Y-%m-%d")):
                        await app.send_message(
                            chat_id=callback_query.from_user.id,
                            text="Ты выбрал дату посещения гостя: %s"
                            % (date.strftime("%Y-%m-%d")),
                            reply_markup=types.ReplyKeyboardRemove(),
                        )
                        setPassRow(
                            callback_query.from_user.id, "date", date.strftime(
                                "%Y-%m-%d")
                        )
                        await app.send_message(
                            callback_query.from_user.id,
                            TIME_MSG,
                            reply_markup=main_menu_markup,
                        )
                        await setUserState(callback_query.from_user.id, "state", 8)
                    else:
                        await app.edit_message_text(
                            callback_query.message.chat.id,
                            callback_query.message.id,
                            "Дата должна быть в будущем!",
                            reply_markup=types.ReplyKeyboardRemove(),
                        )
                        await app.send_message(
                            callback_query.from_user.id,
                            "Выбери правильную дату:",
                            reply_markup=telegramcalendar.create_calendar(),
                        )
            elif state >= 10:
                pass_id = str(callback_query.message.text).split('\n')[0][9:]
                answer = str(callback_query.data)
                if answer == f"['value', '{ACCEPT_BUTTON}', '+']":
                    if await admStatePass(pass_id, 1) == 2:
                        raise "admStatePass() error"
                    else:
                        await app.send_message(callback_query.from_user.id, await getPassByID(pass_id))
                        await app.delete_messages(callback_query.from_user.id, callback_query.message.id)
                elif answer == answer == f"['value', '{DECLINE_BUTTON}', '+']":
                    if await admStatePass(pass_id, 2) == 2:
                        raise "admStatePass() error"
                    else:
                        await app.send_message(callback_query.from_user.id, await getPassByID(pass_id))
                        await app.delete_messages(callback_query.from_user.id, callback_query.message.id)
        except Exception as _ex:
            print_log(f"[Error: old msg ?] {_ex}")


def main():
    os.system("rm -rf 21passbot.*")
    app.run()
    print_log("End!")
