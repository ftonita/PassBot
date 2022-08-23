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

def isaValidDoc(text):
    doc = 0
    doc_number = ""
    try:
        if text.strip()[4] != ' ' or len(text.strip()) != 11:
            raise "spaces"
        text = text.replace(' ', '')
        if len(text) != 10:
            raise
        doc = int(text)
        doc_number = str(f"{str(doc)[:4]} {str(doc)[4:]}")
        return doc_number
    except Exception as _ex:
        print_log(f"[Error] Doc is invalid: {_ex}")
        return ""

def isaValidName(text):
    try:
        num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in num:
            if ' ' not in text.strip() or str(i) in text:
                raise "spaces or numbers"
        return text.strip()
    except Exception as _ex:
        print_log(f"[Error] Doc is invalid: {_ex}")
        return ""