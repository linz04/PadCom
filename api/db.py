import sys
import MySQLdb
import time
from config import app

def connect():
	return (MySQLdb.connect(host="mysql", user="root", passwd="REDACTED", auth_plugin='mysql_native_password', db="padcom"))

def haha():
	return "Test"