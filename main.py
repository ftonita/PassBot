import mysql.connector
from threading import Thread
from classic_utils import print_log
from pyrogram_utils import main, support
from my_socket import localhost

print_log("Hello World!")

try:
    cnx = mysql.connector.connect(
    user="root", password="root", host=localhost, database="21_passbot"
)

    cursor = cnx.cursor()
    print_log("Database connection successful!")
except Exception as _ex:
    print_log(f"Database connect error: {_ex}")

# try:
_observer = Thread(target=support, args=())
_observer.start()
print_log("[OBSERVER] Thread has started!")
main()
_observer.join()
# except Exception as _start:
#     print_log(f"[!!!Error] {_start}")