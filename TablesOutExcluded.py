# TablesOutExcluded.py

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

def DB_get(SQL):
	db = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
						  "Server="+server+";"
						  "Database=Chromium;"
						  "Trusted_Connection=yes;")
	db.autocommit = True

	# Prepare a cursor object using cursor() method
	cursor = db.cursor()
	cursor.execute(SQL)
	result = cursor.fetchall()
	db.close()
	return result

def getCredentials():
	credentialsFile = open(path+os.sep+'DB Setup'+os.sep+'DB Credentials.txt','r')
	server = credentialsFile.readline()
	if server[-1] == '\n':
		server = server[:-1]
	credentialsFile.close()
	return server

def tableOut(info, path):
	fout = open(path, 'w')
	# Loop through dictionary to write to file
	for location in info:
		# Check for none type in object
		if None in location or 'None' in location or 'NULL' in location or 'NULL, NULL' in location:
			# Go through item by item to replace None
			for i in range(len(location)):
				if location[i] == None or location[i] == 'None' or location[i] == 'NULL' or location[i] == 'NULL, NULL':
					location[i] = ''
				elif 'NULL, NULL' in location[i]:
					location[i] = location[i].replace('NULL, NULL, ', '')
				elif 'NULL, ' in location[i]:
					location[i] = location[i].replace('NULL, ', '')
		# Convert list to string
		outLine = '\t'.join(location)
		fout.write(outLine+'\n')
	fout.close()

# ------------------------------------------------------
# OPERATIONS
# ------------------------------------------------------

# Define path
path = os.path.abspath(os.path.dirname(__file__))
# Shorten path to one folder up
path = path[:find_last(path,os.sep)]

# Get DB credentials
server = getCredentials()

excludeInfo = []

# ------------------------------------------------------
# Query out excluded aquifer table
sql = """
SELECT * FROM
	(SELECT * FROM
			chromium_locations 
	WHERE active IS NULL) AS INACTIVE
WHERE substantial_data IS NULL
AND exceedance IS NULL
ORDER BY max DESC, location_id
"""

for row in DB_get(sql):
	excludeInfo.append(row)

# Check that destination directories exist and create if not
if not os.path.exists(path+os.sep+'Locations'+os.sep+'Tables'+os.sep):
	os.makedirs(path+os.sep+'Locations'+os.sep+'Tables'+os.sep)

tableOut(excludeInfo, path+os.sep+'Locations'+os.sep+'Tables'+os.sep+'Excluded.txt')

