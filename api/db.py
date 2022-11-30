import sys
import MySQLdb
import time
from config import app

def connect():
	return (MySQLdb.connect(host="localhost", user="root", passwd="Greyabu@201", auth_plugin='mysql_native_password', db="padcom"))

def haha():
	return "Test"
