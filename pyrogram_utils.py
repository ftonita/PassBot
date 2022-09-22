import asyncio

from includes import *
from classic_utils import *
from mail import *
from mysql_utils import *
from telegramcalendar import *
from monitoring import *


@app.on_message(filters.all)
async def message_handler(client, message):
    text = ""
    try:
        text = str(message.text)
        if '\\' in text:
            text = ""
    except:
        text = ""
    # ПРОВЕРКА НА НАЛИЧИЕ ЮЗЕРА В БД
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
            await database_add_user(user)
            await setUserState(message.from_user.id, "state", 0)
    elif state == 0:
        if (
            STUD_MAIL_ADDRESS in text
            or SCH_MAIL_ADDRESS in text
            and 1 < len(text) < 100
        ):
            print_log(text)
            user.email = str(text.lower())
            user.nickname = text.split("@")[0].lower()
            code = random.randint(100000, 999999)

            print_log("code: " + str(code))
            await simpleMessage(
                app,
                message.from_user.id,
                str("Код подтверждения был отправлен на почту " + user.email + ". Если письмо не пришло, проверь папку 'Спам', а также введенный адрес эл. почты"),
            )
            # отправка сообщения
            print_log(send_email(str(code), user.email))
            # отправка сообщения
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
                await deletePass(message.from_user.id)
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
                pass_.guest_name = isaValidName(text)
                if pass_.guest_name != "":
                    pass_.inviter_id = message.from_user.id
                    pass_.campus = int(await getUserState(message.from_user.id, "campus"))
                    if await database_add_pass(pass_) == 2:
                        await simpleMessage(app, message.from_user.id, "❌ Введи ФИО гостя!")
                        return
                    await setUserState(message.from_user.id, "state", 6)
                    await app.send_message(message.from_user.id, DOCS_MSG, reply_markup=passport_markup)
                else:
                    await simpleMessage(app, message.from_user.id, "❌ Введи ФИО гостя!")    
            else:
                await simpleMessage(app, message.from_user.id, "❌ Введи ФИО гостя!")
        elif state == 6:
            if 1 < len(text) < 100 and text != "None":
                doc_number = str(isaValidDoc(text))
                if doc_number != "":
                    await setPassRow(message.from_user.id, "doc_number", doc_number)
                    await setUserState(message.from_user.id, "state", 7)
                    await app.send_message(message.from_user.id, DATE_MSG, reply_markup=telegramcalendar.create_calendar())
                else:
                    await simpleMessage(app, message.from_user.id, "❌ Введи номер паспорта РФ!\nПример: 1234 567890")
            else:
                await simpleMessage(
                    app,
                    message.from_user.id,
                    "❌ Введи номер паспорта РФ!\nПример: 1234 567890",
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
                    if 10 <= hour <= 18 and text != "None":
                        await setPassRow(message.from_user.id, "hour", hour)
                        await setPassRow(message.from_user.id, "state", 1)
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
                            "Напиши корректное время для посещения: с 10 до 18 часов!",
                        )
                except Exception as _ex:
                    await simpleMessage(
                        app,
                        message.from_user.id,
                        "Напиши корректное время для посещения: с 10 до 18 часов!",
                    )
    #ADM STATE
    elif state >= 10:
        if text == MAIN_MENU_BTN:
            await deletePass(message.from_user.id)
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
                try:
                    await app.send_message(message.chat.id, "🏠 Главное меню", reply_markup=adm_markup)
                except Exception as _ex:
                    print(_ex)

        elif state == 11:
            if text == LAST_PASSES_LIST:
                await simpleMessage(app, message.from_user.id, "📒 Список последних 25 пропусков:")
                await getPassesList(message.from_user.id, 25)
            elif text == CHECK_NEW_PASS:
                new_pass = await admGetPass()
                if new_pass == NO_REQUESTS_FOUND:
                    await app.send_message(message.from_user.id, new_pass)
                else:
                    await app.send_message(message.from_user.id, new_pass, reply_markup=adm_choice_markup)
            elif text == CHECK_PASS:
                await simpleMessage(app, message.from_user.id, "Введи номер пропуска: ")
                await setUserState(message.from_user.id, 'state', 12)
            else:
                await app.send_message(message.from_user.id, "⭐️ Панель Администратора", reply_markup=adm_panel_markup)
        elif state == 12:
            try:
                temp = await getPassByID(int(text))
                if 'В ОБРАБОТКЕ' in temp:
                    await app.send_message(message.from_user.id, temp, reply_markup=adm_choice_markup)
                else:
                    await simpleMessage(app, message.from_user.id, temp)
                    await setUserState(message.from_user.id, 'state', 11)
            except Exception as _ex:
                print_log(f"[Error] {_ex}")
                await simpleMessage(app, message.from_user.id, "❌Введи валидный номер пропуска!")

        

            
    @app.on_callback_query()
    async def CallBackQueryHandler(client, callback_query):
        try:
            state = int(await getUserState(callback_query.from_user.id, "state"))
            if state == 6:
                answer = str(callback_query.data)
                if answer == NO_PASSPORT:
                    await app.send_message(callback_query.from_user.id, "❕ Номер паспорта РФ не указан, при визите гостя нужен документ, подтверждающий его личность!")
                    await app.delete_messages(callback_query.from_user.id, callback_query.message.id)
                    await setPassRow(callback_query.from_user.id, 'doc_number', 'Нет документа')
                    await setUserState(callback_query.from_user.id, 'state', 7)
                    await app.send_message(callback_query.from_user.id, DATE_MSG, reply_markup=telegramcalendar.create_calendar())
            elif state == 7:
                selected, date = await telegramcalendar.process_calendar_selection(
                    app, callback_query
                )
                tmp = datetime.now().date().isoformat()

                if selected:
                    if tmp < str(date.strftime("%Y-%m-%d")):
                        await app.send_message(
                            chat_id=callback_query.from_user.id,
                            text="Ты выбрал дату посещения гостя: %s"
                            % (date.strftime("%Y-%m-%d")),
                            reply_markup=types.ReplyKeyboardRemove(),
                        )
                        await setPassRow(
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
                        await app.send_message(
                            callback_query.from_user.id,
                            "Дата должна быть в будущем!",
                            reply_markup=telegramcalendar.create_calendar(),
                        )
            elif 20 >= state >= 10:
                pass_id = str(callback_query.message.text).split('\n')[0][9:]
                answer = str(callback_query.data)
                if answer == ACCEPT_BUTTON:
                    if await admStatePass(pass_id, 1) == 2:
                        raise "admStatePass() error"
                    else:
                        await app.send_message(callback_query.from_user.id, await getPassByID(pass_id))
                        await app.delete_messages(callback_query.from_user.id, callback_query.message.id)
                        try:
                            await app.send_message(await getPassAuthorByID(pass_id), f"⚡️ОБНОВЛЕН СТАТУС ПРОПУСКА⚡️\n{await getPassByID(pass_id)}")
                        except Exception as _notification:
                            print_log(f"[Error] {_notification}")
                elif answer == DECLINE_BUTTON:
                    if await admStatePass(pass_id, 2) == 2:
                        raise "admStatePass() error"
                    else:
                        await app.send_message(callback_query.from_user.id, await getPassByID(pass_id))
                        await app.delete_messages(callback_query.from_user.id, callback_query.message.id)
                        try:
                            await app.send_message(await getPassAuthorByID(pass_id), f"⚡️ОБНОВЛЕН СТАТУС ПРОПУСКА⚡️\n{await getPassByID(pass_id)}")
                        except Exception as _notification:
                            print_log(f"[Error] {_notification}")
            else:
                await app.delete_messages(callback_query.from_user.id, callback_query.message.id)
        except Exception as _ex:
            print_log(f"[Error: old msg ?] {_ex}")


def main():
    os.system("rm -rf 21passbot.*")
    print_log("[RUN] App is starting!")
    app.run()
    print_log("End!")

def support():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    print_log("[OBSERVER] Observer is running!")
    loop.run_until_complete(observer())
    loop.close()