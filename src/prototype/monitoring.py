from time import sleep
from includes import *
from classic_utils import print_log
from mysql_utils import *
from datetime import datetime

async def observer():
	print_log("[OBSERVER] Observer has started")
	while True:
		sleep(180)
		if cnx:
			date = datetime.now().strftime("%Y-%m-%d")
			hour = int(datetime.now().time().strftime("%H"))
			time = datetime.now().time().strftime("%H:%M")
			minute = int(datetime.now().time().strftime("%M"))
			if 0 <= minute <= 6:
				print_log("Synchronize has started!")
				query = f"SELECT `pass_id` FROM `Passes` WHERE `date` = '{str(date)}' AND `hour` = {str(hour - 1)} AND `status` = '1'"
				cursor = cnx.cursor()
				cursor.execute(query)
				res = cursor.fetchall()
				for i in res:
					print(i[0])
					pass_id = i[0]
					print_log(f"[OBSERVER] pass_id found: {i[0]}-end")
					try:
						await admStatePass(pass_id, 2)
						await app.send_message(await getPassAuthorByID(pass_id), f"⛔️Действие пропуска окончено!\n{await getPassByID(pass_id)}")
						print_log("[OBSERVER] Notification has successfully sent to author!")
					except Exception as _notification:
						print_log(f"[Error] {_notification}")
			print(date, hour, minute)
		else:
			break

