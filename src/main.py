import sys
from threading import Thread
import time
import os

from prototype.dal.mysql_utils import database_connect_attempt
from prototype.gateway.pyrogram_utils import app
from prototype.basicui.classic_utils import print_log

# from basicui.classic_utils import print_log

# from mysql_utils import *
# from classic_utils import *
# from pyrogram_utils import app

if __name__ == '__main__':
	print_log("Hello World!")
	try:
		database_connect_attempt()
	except:	
		print_log("Database connect error")
	
	os.system('rm -rf 21passbot.*')
	app.run()

	print_log("End!")