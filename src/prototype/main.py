import mysql.connector

from classic_utils import print_log
from pyrogram_utils import main
from my_socket import localhost


print_log("Hello World!")

try:
    cnx = mysql.connector.connect(
        user="root",
        password="root",
        host=localhost,
        database="21_passbot"
    )

    cursor = cnx.cursor()
    print_log("Database connection successful!")
except Exception as _ex:
    print_log(f"Database connect error: {_ex}")

main()
