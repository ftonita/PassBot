import datetime


class User:
    def __init__(self):
        self.user_id = -1
        self.verified = -1
        self.nickname = ""
        self.full_name = ""
        self.email = ""
        self.role = -1
        self.campus = -1


class Pass:
    def __init__(self):
        self.inviter_id = ""
        self.doc_number = ""
        self.date = "1970-01-01"
        self.guest_name = ""
        self.hour = 10
        self.status = 0
        self.campus = -1


def print_log(event):
    time = str(datetime.datetime.now())
    log = "[" + time + "] >> " + str(event)
    print(log)


async def simpleMessage(app, id, text):
    await app.send_message(id, text)
