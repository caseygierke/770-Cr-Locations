# Chromium Locations DB Setup.py

# This uses a python connection to SQL Server to set up a 
# new database with a .csv file downloaded from Intellus

# With Notepad++, use F5 then copy this into box
# C:\Users\Casey\Anaconda3\python.exe -i "$(FULL_CURRENT_PATH)"

# ------------------------------------------------------
# IMPORTS
# ------------------------------------------------------

import pyodbc 
from sqlalchemy import create_engine
import urllib
import os
import glob

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
	credentialsFile = open(path+os.sep+'Python'+os.sep+'DB Setup'+os.sep+'DB Credentials.txt','r')
	server = credentialsFile.readline()
	if server[-1] == '\n':
		server = server[:-1]
	credentialsFile.close()
	return server

def getCols(table):
	sql = "SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'"+table+"'"
	colsObject = DB_get(sql)

	# Get table names from tablesObject
	cols = []
	for item in colsObject:
		cols.append(item[3])
	return cols
	
# ------------------------------------------------------
# INPUTS
# ------------------------------------------------------

# Define path
path = os.path.abspath(os.path.dirname(__file__))
# Shorten path to one folder up
path = path[:find_last(path,os.sep)]
# Shorten path to one folder up
path = path[:find_last(path,os.sep)]

# Get DB credentials
server = getCredentials()

# # Get most recent download
# # Read in all .csv file names
# dates = []
# for date in glob.glob(path+os.sep+'Intellus Data'+os.sep+'EIM_EXPORT_*.csv'):
    # # dates.append(date[-8:-4]+date[-14:-12]+date[-11:-9])
	# date = date[-14:-4]
	# dates.append(date[-4:]+date[:2]+date[3:5])

# # Select most recent folder
# downDate = max(dates)

# # Convert back to file format
# downDate = downDate[-4:-2]+'_'+downDate[-2:]+'_'+downDate[:4]

# print('Using input file EIM_EXPORT_'+downDate+'.csv')

# Adjust header row
# Open infile
fin = open(path+os.sep+'Python'+os.sep+'Locations'+os.sep+'Outputs'+os.sep+'Compiled- Narrowed- For DB.txt','r')
# Open the file to write to
fout = open(path+os.sep+'Python'+os.sep+'Locations'+os.sep+'Outputs'+os.sep+'DBin.csv','w')

# Loop through file to fix header row
for line in fin:
	cols = line.split('\t')
	if cols[0] == 'Location ID':
		# print(line)
		cols = line
		cols = cols.replace(' ','_')
		cols = cols.lower()
		line = cols
		header = cols
	
	# Write to file
	fout.write(line)
	
# Close files
fin.close()
fout.close()

# Change filePath to be SQL compatible
filePath = path+os.sep+'Python'+os.sep+'Locations'+os.sep+'Outputs'+os.sep+'DBin.csv'
filePath = filePath.replace(os.sep, '/')

# Designat table name
table = 'chromium_locations'

# -- ------------------------------------------------------
# -- 1. Import data to Chromium table
# -- ------------------------------------------------------

# -- Create a new Chromium DB
sql = 'USE [Chromium]'
DB(sql)

sql = '''DROP TABLE IF EXISTS chromium_locations;
	CREATE TABLE chromium_locations (
	location_id VARCHAR(100), 
	aquifer VARCHAR(100), 
	latitude VARCHAR(100), 
	longitude VARCHAR(100), 
	ground_elevation VARCHAR(100), 
	geologic_unit_code VARCHAR(100), 
	well_installation_date VARCHAR(100),
	total_well_depth VARCHAR(100), 
	well_diameter VARCHAR(100), 
	screen_top VARCHAR(100), 
	screen_bottom VARCHAR(100), 
	comments VARCHAR(1000), 
	well_completion_report_url VARCHAR(100), 
	location_type VARCHAR(100), 
	monitoring_area VARCHAR(100), 
	watershed VARCHAR(100), 
	well_status VARCHAR(100), 
	inactive_date VARCHAR(100), 
	toc_elevation VARCHAR(100), 
	lwa_notes VARCHAR(500), 
	source VARCHAR(100), 
	max_date VARCHAR(100),
	max VARCHAR(100),
	active VARCHAR(100),
	exceedance VARCHAR(100),
	substantial_data VARCHAR(100))'''
DB(sql)

# DROP TABLE IF EXISTS IEc_SLVs;
	# CREATE TABLE IEc_SLVs (PARAMETER_CODE VARCHAR(20), SLVAnalysis FLOAT, SLVUnits VARCHAR(10), FILTERED_FLAG VARCHAR(10), Source VARCHAR(500));
	# BULK INSERT dbo.IEc_SLVs 
	# FROM 'C:\Projects\\770- LANL\Chromium\\2020\Python\DB Setup\IEc_SLVs.txt'
	# WITH ( FIELDTERMINATOR = '\t', FIRSTROW = 2 );

# # -- Dynamically create a new Chromium table and get column names
# sql = """DECLARE @sql NVARCHAR(MAX)
# -- DECLARE @filePath NVARCHAR(MAX) = 'C:/Projects/770- LANL/Chromium/2020/Intellus Data/DBin.csv'
# DECLARE @filePath NVARCHAR(MAX) = '"""+filePath+"""'
# DECLARE @tableName NVARCHAR(MAX) = '"""+table+"""'
# DECLARE @colString NVARCHAR(MAX)

# SET @sql = 'SELECT @res = LEFT(BulkColumn, CHARINDEX(CHAR(10),BulkColumn)) FROM  OPENROWSET(BULK ''' + @filePath + ''', SINGLE_CLOB) AS x'
# exec sp_executesql @sql, N'@res NVARCHAR(MAX) output', @colString output;

# SELECT @sql = 'DROP TABLE IF EXISTS ' + @tableName + ';  CREATE TABLE [dbo].[' + @tableName + ']( ' + STRING_AGG(name, ', ') + ' ) '
# FROM (
    # SELECT ' [' + value + '] nvarchar(max) ' as name
    # FROM STRING_SPLIT(@colString, ',')
# ) t

# EXECUTE(@sql)"""
# DB(sql)

# Trying to rename the last column programmatically
# cols = getCols('RAW')
# # Change last column name to drop the \n
# sql = "EXEC sp_RENAME '[Chromium].[dbo].[Chromium]."+cols[-1]+"' , 'VALIDATION_REASON_CODES', 'COLUMN'"
# DB(sql)

# # Change filePath to be SQL compatible
# fin = open(path+os.sep+'Python'+os.sep+'Locations'+os.sep+'Outputs'+os.sep+'Watersheds- Final- Compiled- Narrowed.txt','r')

filePath = path+os.sep+'Python'+os.sep+'Locations'+os.sep+'Outputs'+os.sep+'Compiled- Narrowed- For DB.txt'
filePath = filePath.replace(os.sep, '/')

# -- Import from .csv file to table
sql = """BULK INSERT dbo."""+table+"""
FROM '"""+filePath+"""'
WITH ( FIELDTERMINATOR = '\t', FIRSTROW = 2 );
"""
DB(sql)

# # Change last column name to drop the \n
# sql = """EXEC sp_RENAME '[Chromium].[dbo].[Chromium].VALIDATION_REASON_CODES\n' , 'VALIDATION_REASON_CODES', 'COLUMN'"""
# DB(sql)

