from email.message import Message
from classic_utils import *

from pyrogram import Client, filters, types
import tgcrypto
import asyncio
import random

from mysql_utils import *

api_id = 10439243 #API id
api_hash = "a98d30318fc4d1cd274bc750fa34c8b9" #API hash
bot_token = "5761358088:AAGoBiwLt69qRkI439sKdfCz__tCS3jRLNk"

app = Client(
	"21passbot",
	api_id=api_id,
	api_hash=api_hash,
	bot_token=bot_token
)

START_CMD = "/start"

HELLO_TXT = "Привет, я - бот Школы 21 для приглашения гостей в школу. Для авторизации напиши свою школьную почту (@student.21-school.ru - для студентов, @21-school.ru - для персонала)"

STUD_MAIL_ADDRESS = "@student.21-school.ru"
SCH_MAIL_ADDRESS = "@21-school.ru"
MAIL_HAS_SENT = "Введи код подтверждения, отправленный на почту!"

CREATE_PASS_BUTTON = "✅Создать пропуск"
VIEW_MY_PASS_BUTTON = "📄Мои пропуски"

active_users = []

async def getUserState(user_id, row):
	state = database_select_user_row(user_id, row)
	return state

async def getPassState(pass_id, row):
	state = database_select_pass_row(pass_id, row)
	return state

async def simpleMessage(message, text):
	await app.send_message(message.chat.id, text)

@app.on_message(filters.all)
async def message_handler(client, message):
	text = ""
	try:
		text = str(message.text)
	except:
		pass
# ЗДЕСЬ БУДЕТ ПРОВЕРКА НА НАЛИЧИЕ ЮЗЕРА В БД
	state = int(await getUserState(message.from_user.id, 'state'))
	user = User()
	user.user_id = message.from_user.id
	if state == -1:
		if text == START_CMD:
			await simpleMessage(message, HELLO_TXT)
			user.campus = -1
			user.full_name = ""
			user.role = 1
			database_add_user(user)
			setUserState(message.from_user.id, 'state', 0)
	elif state == 0:
		if STUD_MAIL_ADDRESS in text or SCH_MAIL_ADDRESS in text:
			await simpleMessage(message, MAIL_HAS_SENT)
			print_log(text)
			user.email = text
			user.nickname = text.split("@")[0]
			code = random.randint(100000, 999999)

			print_log("code: " + str(code))
			# отправка сообщения
			await simpleMessage(message, str("Код подтверждения был отправлен на почту " + text))
			setUserState(message.from_user.id, 'email', user.email)
			setUserState(message.from_user.id, 'nickname', user.nickname)
			setUserState(message.from_user.id, 'code', code)
			setUserState(message.from_user.id, 'state', 1)
		else:
			await simpleMessage(message, "Для авторизации напиши свою школьную почту (@student.21-school.ru - для студентов, @21-school.ru - для персонала")
	elif state == 1:
		print("TMP: ", int(await getUserState(message.from_user.id, 'code')))
		tmp = str(await getUserState(message.from_user.id, 'code'))
		if tmp in text:
			setUserState(message.from_user.id, 'state', 2)
			await simpleMessage(message, "Авторизация прошла успешно")
			await simpleMessage(message, "Введи своё имя (желательно ФИО)")
		else:
			setUserState(message.from_user.id, 'state', 0)
			await simpleMessage(message, "Неверный код подтверждения! Введи почту еще раз!")
	elif state == 2:
		if len(text) > 1:
			user.full_name = text
			setUserState(message.from_user.id, 'full_name', user.full_name)
			setUserState(message.from_user.id, 'state', 3)
			await simpleMessage(message, "Из какого ты кампуса(напиши: msc/kzn/nsk)?")
		else:
			await simpleMessage(message, "Требуется ввести своё имя!")
	elif state == 3:
		if len(text) > 1:
			if 'msk' in text.lower():
				user.campus = 1
			elif 'kzn' in text.lower():
				user.campus = 2
			elif 'nsk' in text.lower():
				user.campus = 3
			else:
				await simpleMessage(message, "Некорректный ввод кампуса!\nОбразец: msc/kzn/nsk")
				return
			setUserState(message.from_user.id, 'campus', user.campus)
			setUserState(message.from_user.id, 'state', 4)
			create_pass_button = types.KeyboardButton(CREATE_PASS_BUTTON)
			my_passes_button = types.KeyboardButton(VIEW_MY_PASS_BUTTON)
			markup = types.ReplyKeyboardMarkup(keyboard=[[create_pass_button, my_passes_button]], resize_keyboard=True)
			await app.send_message(message.chat.id, "Регистрация прошла успешно!", reply_markup=markup)
	elif state >= 4:
		if text == CREATE_PASS_BUTTON:
			await simpleMessage(message, "Введи ФИО гостя! Если гостей несколько, пиши через запятую.\nВажно: при отсутствии одной из части имени тебе могут ОТКАЗАТЬ в пропуске!")
		elif text == VIEW_MY_PASS_BUTTON:
			await simpleMessage(message, "Список твоих пропусков")
		else:
			create_pass_button = types.KeyboardButton(CREATE_PASS_BUTTON)
			my_passes_button = types.KeyboardButton(VIEW_MY_PASS_BUTTON)
			markup = types.ReplyKeyboardMarkup(keyboard=[[create_pass_button, my_passes_button]], resize_keyboard=True)
			await app.send_message(message.chat.id, "Нажми на кнопку!", reply_markup=markup)
