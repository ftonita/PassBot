import os
import random
import tgcrypto
from pyrogram import Client, filters, types
from pyrogram.types import KeyboardButton
import pyqrcode as pq
import telegramcalendar

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

NAME_MSG = "Введи Фамилию, Имя и Отчество (при наличии) гостя, пожалуйста!"
DOCS_MSG = "Это точно реальный человек? :) Введи номер паспорта (пример: 1234 567890)"
DATE_MSG = "Отлично! Теперь нам нужно знать, когда твой гость планирует посетить школу. Выбери нужную дату"
TIME_MSG = "Почти закончили! Подскажи, во сколько (с 10:00 до 18:00) планирует прийти твой гость? (укажи только " \
           "час, например, 15 будет означать 15:00) "
BYE_MSG = (
    "Суперски! Запрос отправлен. Теперь нужно немножко подождать, пока АДМ его одобрят!"
)

RULE_34 = "Обрати внимание на несколько правил: Гостей можно приводить с 10:00 до 19:00 в будние дни\n1 участник за " \
          "одно посещение может привести не более 2 гостей\nПродолжительность визита - не более 1 часа\nНа территории " \
          "«Школы 21» каждый гость должен быть всегда в сопровождении участника\nНужно заполнить эту гугл-форму не " \
          "позднее, чем за 1 день до визита в рабочее время (пн - пт с 10:00 до 19:00)\nНа входе гостю необходимо " \
          "предъявить паспорт "

NO_PASSPORT = "У гостя нет паспорта РФ🇷🇺"

LAST_PASSES_LIST = "📒Список последних 25 пропусков"
CHECK_NEW_PASS = "📄 Обработать заявку"
CHECK_PASS = "🔍 Поиск по номеру пропуска"

NO_REQUESTS_FOUND = "📄 Нет необработанных заявок!"

ACCEPT_BUTTON = "✅ ПРИНЯТЬ"
DECLINE_BUTTON = "❌ ОТКЛОНИТЬ"

main_menu_button = types.KeyboardButton(MAIN_MENU_BTN)

create_pass_button: KeyboardButton = types.KeyboardButton(CREATE_PASS_BUTTON)
my_passes_button = types.KeyboardButton(VIEW_MY_PASS_BUTTON)
no_passport_button = types.InlineKeyboardButton(text=NO_PASSPORT, callback_data=NO_PASSPORT)

adm_button = types.KeyboardButton(ADM_MM)
view_all = types.KeyboardButton(LAST_PASSES_LIST)
get_one = types.KeyboardButton(CHECK_NEW_PASS)
get_one_byID = types.KeyboardButton(CHECK_PASS)

accept_button = types.InlineKeyboardButton(text=ACCEPT_BUTTON, callback_data=ACCEPT_BUTTON)
decline_button = types.InlineKeyboardButton(text=DECLINE_BUTTON, callback_data=DECLINE_BUTTON)

adm_choice_markup = types.InlineKeyboardMarkup([[accept_button],[decline_button]])

markup = types.ReplyKeyboardMarkup(
    keyboard=[[create_pass_button, my_passes_button]], resize_keyboard=True
)

passport_markup = types.InlineKeyboardMarkup([[no_passport_button]])

adm_markup = types.ReplyKeyboardMarkup(
    keyboard=[[adm_button], [create_pass_button, my_passes_button]], resize_keyboard=True
)

adm_panel_markup = types.ReplyKeyboardMarkup(
    keyboard=[[view_all], [get_one], [get_one_byID], [main_menu_button]], resize_keyboard=True
)

main_menu_markup = types.ReplyKeyboardMarkup(
    keyboard=[[main_menu_button]], resize_keyboard=True
)
