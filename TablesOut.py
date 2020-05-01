# TablesOut.py

# This uses a python connection to SQL Server to query out
# informations for the LWA chromium report table

# With Notepad++, use F5 then copy this into box
# C:\Users\Casey\Anaconda3\python.exe -i "$(FULL_CURRENT_PATH)"
# C:\ProgramData\Anaconda3\python.exe -i "$(FULL_CURRENT_PATH)"

# ------------------------------------------------------
# IMPORTS
# ------------------------------------------------------

import pyodbc 
from sqlalchemy import create_engine
# import urllib
import os
# import glob

# ------------------------------------------------------
# DEFINE FUNCTIONS
# ------------------------------------------------------

# Define last position finder
def find_last(s,t):
	last_pos = -1
	while True:
		pos = s.find(t, last_pos +1)
		if pos == -1:
			return last_pos
		last_pos = pos

# Define a database command
def DB(SQL):
	# connection = pymysql.connect(host='localhost', user='root', password='Phr3atic', db=database, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor, local_infile=True)
	cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
						  "Server="+server+";"
						  "Database=Chromium;"
						  "Trusted_Connection=yes;")
	try:
		with cnxn.cursor() as cursor:
			cursor.execute(SQL)
		cnxn.commit()
	finally:
		cnxn.close()

# def DB_get(SQL):
	# db = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
						  # "Server="+server+";"
						  # "Database=Chromium;"
						  # "Trusted_Connection=yes;")
	# db.autocommit = True

	# # Prepare a cursor object using cursor() method
	# cursor = db.cursor()
	# cursor.execute(SQL)
	# result = cursor.fetchall()
	# db.close()
	# return result

# def getTables():
	# sql = "SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'"
	# tableObject = DB_get(sql)

	# # Get table names from tablesObject
	# tables = []
	# for item in tableObject:
		# tables.append(item[2])
	# return tables
	
# def getCols(table):
	# sql = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'"+table+"'"
	# colsObject = DB_get(sql)

	# # Get table names from tablesObject
	# cols = []
	# for item in colsObject:
		# cols.append(item[3])
	# return cols

def getCredentials():
	credentialsFile = open(path+os.sep+'DB Setup'+os.sep+'DB Credentials.txt','r')
	server = credentialsFile.readline()
	if server[-1] == '\n':
		server = server[:-1]
	credentialsFile.close()
	return server

# ------------------------------------------------------
# OPERATIONS
# ------------------------------------------------------

# Define path
path = os.path.abspath(os.path.dirname(__file__))
# Shorten path to one folder up
path = path[:find_last(path,os.sep)]

# Get DB credentials
server = getCredentials()
