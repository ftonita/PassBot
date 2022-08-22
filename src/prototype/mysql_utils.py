import mysql.connector
from my_socket import localhost
from classic_utils import *


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


def database_add_user(user):
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


def database_add_pass(pass_):
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


def setPassRow(user_id, char, value):
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

def deletePass(inviter_id):
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


