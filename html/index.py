from flask import Flask, render_template, request
import datetime
import mysql.connector

app = Flask(__name__, template_folder='./templates',static_folder='./static')


cnx = mysql.connector.connect(
    user="R6teZRU0Le", password="CjhGc1UktN", host="remotemysql.com", database="R6teZRU0Le"
    )

def print_log(event):
    time = str(datetime.datetime.now())
    log = "WEB [" + time + "] >> " + str(event)
    print(log)

class Pass():
    def __init__(self):
        self.pass_id = "-1"
        self.name = "No Name"
        self.doc_number = "None"
        self.date = "None"
        self.time = "00"
        self.status = "None"
        self.inviter = "None"

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


def getUserState(user_id, row):
    state = database_select_user_row(user_id, row)
    return state

def getPassByID(pass_id):
    cursor = cnx.cursor()
    print_log("Database connection successful!")
    try:
        query = "SELECT * FROM `Passes` WHERE `pass_id` = " + str(pass_id)
        cursor.execute(query)
        res = cursor.fetchall()
        tmp = Pass()
        if len(res) == 0:
            return tmp
        else:
            for i in res:
                if str(i[6]) == '0':
                    tmp.status = "🔵 В ОБРАБОТКЕ"
                elif str(i[6]) == '1':
                    tmp.status = "🟢 ОДОБРЕН"
                elif str(i[6]) >= '2':
                    tmp.status = "🔴 НЕДЕЙСТВИТЕЛЕН"
                tmp.pass_id = str(i[0])
                tmp.name =  str(i[2])
                tmp.doc_number = str(i[3])
                tmp.date = str(i[4])
                tmp.time = str(i[5])
                tmp.inviter = getUserState(str(i[1]), 'nickname')
        print_log("Passes have selected successful or no passes have found!")
    except Exception as ex:
        print_log("[Error] Passes list select error: ")
        print_log(ex)
    cursor.close()
    return tmp


@app.route('/')
def index():
	pass_info = Pass()
	return render_template('index.html', pass_id=pass_info.pass_id, name=pass_info.name, doc_number=pass_info.doc_number, date=pass_info.date, time=pass_info.time, status=pass_info.status, inviter=pass_info.inviter)

@app.route('/pass', methods=['GET'])
def sample():
    pass_info = Pass()
    try:
        tmp = request.args.get('pass_id')
        print(f"TMP: {tmp}")
        pass_info = getPassByID(int(tmp))
    except Exception as _ex:
        print_log(f"[Error-Web] {_ex}")
    finally:
        return render_template('index.html', pass_id=pass_info.pass_id, name=pass_info.name, doc_number=pass_info.doc_number, date=pass_info.date, time=pass_info.time, status=pass_info.status, inviter=pass_info.inviter)



if __name__ == '__main__':
	app.run()