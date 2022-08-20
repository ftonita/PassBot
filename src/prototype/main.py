import sys
from threading import Thread
import time


from mysql_utils import *
from classic_utils import *
from pyrogram_utils import app

if __name__ == '__main__':
	print_log("Hello World!")
	try:
		database_connect_attempt()
	except:	
		print_log("Database connect error")
	
	os.system('rm -rf 21passbot.*')
	app.run()

	print_log("End!")