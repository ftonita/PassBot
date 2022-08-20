from curses.ascii import isalnum
import sys
import mysql.connector

from classic_utils import *

cnx = mysql.connector.connect(user='root', password='root',
							host='10.178.131.232',
							database='21_passbot')

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
		query = "INSERT INTO `Users`(`user_id`, `nickname`, `full_name`, `email`, `role`, `campus`, `state`, `code`) VALUES ('"+ str(user.user_id) +"','"+ user.nickname +"','"+ user.full_name +"','"+ user.email +"','"+ str(user.role) +"','"+str(user.campus)+"', '-1', '0')"
		cursor.execute(query)
		cnx.commit()
		print_log("User has added to database successful!")
	except Exception as ex:
		print_log("[Error] User has not added to database!")
		print_log(ex)
	# finally:
	# 	if (cnx):
	# 		cursor.close()
	# 		cnx.close()

def database_select_user_row(user_id, row):
	cursor = cnx.cursor()
	print_log("Database connection successful!")
	try:
		query = "SELECT `" + row + "` FROM `Users` WHERE `user_id` = "+ str(user_id)
		cursor.execute(query)
		res = cursor.fetchone()
		if (res is None):
			print("cursor fetch res: " + str(cursor.fetchone()))
			res = -1
		else:
			res = res[0]
		print_log("User has selected successful or no users have found!")
		cursor.close()
	except Exception as ex:
		print_log("[Error] User select error: ")
		print_log(ex)
	return res


def setUserState(user_id, char, state):
	cursor = cnx.cursor()
	print_log("Database connection successful!")
	try:
		query = "UPDATE `Users` SET `" + char + "`='" + str(state) + "' WHERE `user_id` = "+ str(user_id)
		cursor.execute(query)
		cnx.commit()
		print_log("User char/state has updated successful!")
	except Exception as ex:
		print_log("[Error] User char/state has not updated!")
		print_log(ex)

def database_add_pass(pass_):
	cursor = cnx.cursor()
	print_log("Database connection successful!")
	try:
		query = "INSERT INTO `Users`(`pass_id`, `inviter_id`, `guest_name`, `start_datetime`, `duration`, `status`, `campus`) VALUES ('"+ str(pass_.pass_id) +"','"+ pass_.inviter_id +"','"+ pass_.guest_name +"','"+ str(pass_.start_datetime) +"','"+ str(pass_.duration) +"','"+str(pass_.status)+"', '"+str(pass_.campus)+"')"
		cursor.execute(query)
		cnx.commit()
		print_log("Pass has added to database successful!")
	except Exception as ex:
		print_log("[Error] Pass has not added to database!")
		print_log(ex)

def database_select_pass_row(pass_id, row):
	cursor = cnx.cursor()
	print_log("Database connection successful!")
	try:
		query = "SELECT `" + row + "` FROM `Passes` WHERE `pass_id` = "+ str(pass_id)
		cursor.execute(query)
		res = cursor.fetchone()
		if (res is None):
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

def setPassState(pass_id, char, state):
	cursor = cnx.cursor()
	print_log("Database connection successful!")
	try:
		query = "UPDATE `Passes` SET `" + char + "`='" + str(state) + "' WHERE `pass_id` = "+ str(pass_id)
		cursor.execute(query)
		cnx.commit()
		print_log("Pass char/state has updated successful!")
	except Exception as ex:
		print_log("[Error] Pass char/state has not updated!")
		print_log(ex)