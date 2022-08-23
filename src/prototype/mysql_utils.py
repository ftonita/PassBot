import mysql.connector
from my_socket import localhost
from includes import *
from classic_utils import *
from json_utils import *

cnx = mysql.connector.connect(
    user="root", password="root", host=localhost, database="21_passbot"
)


def database_connect_attempt():
    cursor = cnx.cursor()
    print_log("Database connection successful!")
    # if (cnx):
    # 	cursor.close()
    # 	cnx.close()
    return 0


async def database_add_user(user):
    cursor = cnx.cursor()
    print_log("Database connection successful!")
    try:
        query = (
            "INSERT INTO `Users`(`user_id`, `nickname`, `full_name`, `email`, `role`, `campus`, `state`, `code`) VALUES ('"
            + str(user.user_id)
            + "','"
            + user.nickname
            + "','"
            + user.full_name
            + "','"
            + user.email
            + "','"
            + str(user.role)
            + "','"
            + str(user.campus)
            + "', '-1', '0')"
        )
        cursor.execute(query)
        cnx.commit()
        print_log("User has added to database successful!")
    except Exception as ex:
        print_log("[Error] User has not added to database!")
        print_log(ex)
        cursor.close()
        return 2
    cursor.close()
    # finally:
    # 	if (cnx):
    # 		cursor.close()
    # 		cnx.close()


def database_select_user_row(user_id, row):
    cursor = cnx.cursor()
    print_log("Database connection successful!")
    try:
        query = "SELECT `" + row + \
            "` FROM `Users` WHERE `user_id` = " + str(user_id)
        cursor.execute(query)
        res = cursor.fetchone()
        if res is None:
            print("cursor fetch res: " + str(cursor.fetchone()))
            res = -1
        else:
            res = res[0]
        print_log("User has selected successful or no users have found!")
    except Exception as ex:
        print_log("[Error] User select error: ")
        print_log(ex)
    cursor.close()
    return res


async def setUserState(user_id, char, state):
    cursor = cnx.cursor()
    print_log("Database connection successful!")
    try:
        query = (
            "UPDATE `Users` SET `"
            + char
            + "`='"
            + str(state)
            + "' WHERE `user_id` = "
            + str(user_id)
        )
        cursor.execute(query)
        cnx.commit()
        print_log("User char/state has updated successful!")
    except Exception as ex:
        print_log("[Error] User char/state has not updated!")
        print_log(ex)
        cursor.close()
        return 2
    cursor.close()


async def database_add_pass(pass_):
    cursor = cnx.cursor()
    print_log("Database connection successful!")
    try:
        query = (
            "INSERT INTO `Passes`(`inviter_id`, `guest_name`, `doc_number`, `date`, `hour`, `status`, `campus`, "
            "`state`) VALUES (' "
            + str(pass_.inviter_id)
            + "','"
            + str(pass_.guest_name)
            + "','None','2000-01-01', '10','0', '"
            + str(pass_.campus)
            + "', '-1')"
        )
        cursor.execute(query)
        cnx.commit()
        print_log("Pass has added to database successful!")
    except Exception as ex:
        print_log("[Error] Pass has not added to database!")
        print_log(ex)
        cursor.close()
        return 2
    cursor.close()


async def setPassRow(user_id, char, value):
    cursor = cnx.cursor()
    print_log("Database connection successful!")
    try:
        query = (
            "UPDATE `Passes` SET `"
            + char
            + "`='"
            + str(value)
            + "' WHERE `inviter_id` = "
            + str(user_id)
            + " AND `state` = '-1'"
        )
        cursor.execute(query)
        cnx.commit()
        print_log("Pass char/state has updated successful!")
    except Exception as ex:
        print_log("[Error] Pass char/state has not updated!")
        print_log(ex)
        cursor.close()
        return 2
    cursor.close()

async def deletePass(inviter_id):
    cursor = cnx.cursor()
    print_log("Database connection successful!")
    try:
        query = ("DELETE FROM `Passes` WHERE `inviter_id` = " + str(inviter_id) + " AND `state` = '-1'")
        cursor.execute(query)
        cnx.commit()
        print_log("Pass has deleted successful!")
    except Exception as ex:
        print_log("[Error] Pass has not deleted!")
        print_log(ex)
        cursor.close()
        return 2
    cursor.close()

async def admStatePass(pass_id, value):
    cursor = cnx.cursor()
    print_log("[ADM] Database connection successful!")
    try:
        query = ("UPDATE `Passes` SET `status` = '"+ str(value) + "' WHERE `pass_id` = '" + str(pass_id) + "'")
        cursor.execute(query)
        cnx.commit()
        print_log("[ADM] Pass status has updated successful!")
    except Exception as ex:
        print_log("[Error][ADM] Pass status has not updated!")
        print_log(ex)
        cursor.close()
        return 2
    cursor.close()


async def getUserState(user_id, row):
    state = database_select_user_row(user_id, row)
    return state


async def admGetPass():
    cursor = cnx.cursor()
    print_log("Database connection successful!")
    try:
        query = "SELECT * FROM `Passes` WHERE `status` = '0' LIMIT 1"
        cursor.execute(query)
        res = cursor.fetchall()
        if len(res) == 0:
            tmp = NO_REQUESTS_FOUND
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
        campus = str(await getUserState(user_id, 'campus'))
        query = "SELECT * FROM `Passes` WHERE `campus` = '"+ campus +"' ORDER BY `pass_id` DESC LIMIT 25"
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
        tmp = ""
        stat = ""
        if len(res) == 0:
            tmp = "📄 Пропуск не найден!"
        else:
            for i in res:
                if str(i[6]) == '0':
                    stat = "🔵 В ОБРАБОТКЕ"
                elif str(i[6]) == '1':
                    stat = "🟢 ОДОБРЕН"
                elif str(i[6]) >= '2':
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
                res = pq.create(f"http://localhost:8080/index.html?pass_id={value}")
                res.png(f'cache/{value}.png', scale=8)
                with open(f'cache/{value}.png', 'rb') as photo:
                    await app.send_media_group(user_id, [types.InputMediaPhoto(photo, caption=tmp)])
                os.system(f'rm -rf cache/{value}.png')
                # JSON
                await createJSON([
                    str(i[0]),
                    str(i[2]),
                    str(i[3]),
                    str(i[4]),
                    str(i[5]),
                    stat,
                    await getUserState(await getPassAuthorByID(str(i[0])), 'nickname'),
                ])
                # JSON
        print_log("Passes have selected successful or no users have found!")
    except Exception as ex:
        print_log("[Error] Passes list select error: ")
        print_log(ex)
    cursor.close()


async def getPassAuthorByID(pass_id):
    cursor = cnx.cursor()
    print_log("Database connection successful!")
    try:
        tmp = ""
        query = "SELECT `inviter_id` FROM `Passes` WHERE `pass_id` = " + str(pass_id)
        cursor.execute(query)
        res = cursor.fetchone()
        if res != None:
            tmp = str(res[0]).strip()
        print_log("Passes have selected successful or no passes have found!")
    except Exception as ex:
        print_log("[Error] Passes list select error: ")
        print_log(ex)
        tmp = ""
    cursor.close()
    return tmp
