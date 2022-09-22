from mysql_utils import *
from classic_utils import *


def setPassStateByID(pass_id, char, state):
    cursor = cnx.cursor()
    print_log("Database connection successful!")
    try:
        query = "UPDATE `Passes` SET `" + char + "`='" + \
            str(state) + "' WHERE `pass_id` = " + str(pass_id)
        cursor.execute(query)
        cnx.commit()
        print_log("Pass char/state has updated successful!")
    except Exception as ex:
        print_log("[Error] Pass char/state has not updated!")
        print_log(ex)


def getPassRowById(pass_id, row):
    cursor = cnx.cursor()
    print_log("Database connection successful!")
    res = 0
    try:
        query = "SELECT `" + row + \
            "` FROM `Passes` WHERE `pass_id` = " + str(pass_id)
        res = cursor.fetchone()
        cursor.execute(query)
        if res is None:
            print("cursor fetch res: " + str(cursor.fetchone()))
            res = -1
        else:
            res = res[0]
        print_log("Pass has selected successful or no passes have found!")
        cursor.close()
    except Exception as ex:
        print_log("[Error] Pass select error: ")
        print_log(ex)
    return res
