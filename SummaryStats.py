# SummaryStats.py

# This code generates summary statistics for locations 
# in the file specified 

# Written by Casey Gierke of Lee Wilson & Associates
# on 4/8/2020

# With Notepad++, use F5 then copy this into box
# C:\Users\Casey\Anaconda3\python.exe -i "$(FULL_CURRENT_PATH)"

# ------------------------------------------------------
# IMPORTS
# ------------------------------------------------------

import datetime
import os
import pyodbc
import statistics
import matplotlib.pyplot as plt
import seaborn as sns

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

# Define path
path = os.path.abspath(os.path.dirname(__file__))
# Shorten path to one folder up
path = path[:find_last(path,os.sep)]
# Shorten path to one folder up
path = path[:find_last(path,os.sep)]

# Get DB credentials
server = getCredentials()

# DB setup
sql_conn = pyodbc.connect('DRIVER={ODBC Driver 13 for SQL Server};'
							"Server="+server+";"
							'DATABASE=Chromium;'
							'Trusted_Connection=yes') 

def getCredentials():
	credentialsFile = open(path+os.sep+'Python'+os.sep+'DB Setup'+os.sep+'DB Credentials.txt','r')
	server = credentialsFile.readline()
	if server[-1] == '\n':
		server = server[:-1]
	credentialsFile.close()
	return server

# ------------------------------------------------------
# INPUTS
# ------------------------------------------------------

# Define input file
input = 'Compiled- Narrowed'
# input = 'Plume- Compiled- Regional'
inputPath = path+os.sep+'Python'+os.sep+'Locations'+os.sep+'Outputs'+os.sep

# Define subThreshold value (number of data points to be substantial)
subThreshold = 5

# Make dictionary for appendix figures
figureDict = {}
Dictin = open(inputPath+input+'.txt','r')

# Get first line
cols = Dictin.readline()
cols = cols.split('\t')
headers = cols

# # Get desired indices from header row
locID_index = headers.index('Location ID')
lat_index = headers.index('Latitude')
long_index = headers.index('Longitude')
type_index = headers.index('Aquifer')

# Read in data
for line in Dictin:
	Columns = line.split('\t')
	figureDict[Columns[0]] = {'Lat': Columns[lat_index], 'Long': Columns[long_index], 'Aquifer': Columns[type_index]}
	
# # Short circuit
# figureDict = {'SIMR-2': figureDict['SIMR-2']}

# Create an outfile for storing maxes
fout = open(path+os.sep+'Python'+os.sep+'Locations'+os.sep+'Outputs'+os.sep+'Maxes- '+input+'.txt','w')

# Create an outfile for storing maxes
foutExceedance = open(path+os.sep+'Python'+os.sep+'Locations'+os.sep+'Outputs'+os.sep+'Exceedance- '+input+'.txt','w')
exceedance = []

# Create an outfile for defining active locations
foutActive = open(path+os.sep+'Python'+os.sep+'Locations'+os.sep+'Outputs'+os.sep+'Active- '+input+'.txt','w')

# Create an outfile for defining active locations
foutSubstantial = open(path+os.sep+'Python'+os.sep+'Locations'+os.sep+'Outputs'+os.sep+'Substantial Data- '+input+'.txt','w')
subNum = []

# ------------------------------------------------------
# COMPUTATIONS
# ------------------------------------------------------

# Define SLV value
SLV = 7.48

# Loop over inputs
for location in figureDict:

	print('Working on '+location)

	# Query out data
	sql = "SELECT SAMPLE_DATE, REPORT_RESULT AS Data, DETECTED, FILTERED FROM Chromium_Flagged WHERE LOCATION_ID = '"+location+"' ORDER BY SAMPLE_DATE"
	data = DB_get(sql)
		
	# Initialize arrays
	date = []
	result = []
	ND = []
	F = []
	daysND = []
	dataND = []
	daysF = []
	dataF = []

	# Loop through data
	for row in data:
		
		# Append values
		date.append(row[0])
		result.append(float(row[1]))
		ND.append(row[2])
		F.append(row[3])
		
		# Check for non-detects
		if row[2] == 'N':
			daysND.append(row[0])
			dataND.append(float(row[1]))
		# Check for filtering
		if row[3] == 'Y':
			daysF.append(row[0])
			dataF.append(float(row[1]))
	
	# ------------------------------------------------------
	# OUTPUTS
	# ------------------------------------------------------
	
	# Check if result has values
	if result == []:
		maxResult = 'No Data'
		maxDate = 'No Data'
		maxND = 'No Data'
		maxF = 'No Data'
	else:
		# Get max
		maxResult = max(result)
		maxIndex = result.index(maxResult)
		maxDate = date[maxIndex]
		maxND = ND[maxIndex]
		maxF = F[maxIndex]
	
		# Write exceedances to outfile
		if float(maxResult) > SLV:
			foutExceedance.write(location+'\t'+figureDict[location]['Long']+'\t'+figureDict[location]['Lat']+'\t'+str(maxDate)+'\t'+str(maxResult)+'\t'+maxND+'\t'+maxF+'\t'+str(len(result))+'\n')
			# Append to exceedance list
			for item in result:
				exceedance.append(item)

		# Check if active
		if datetime.datetime(max(date).year, max(date).month, max(date).day) > datetime.datetime.strptime('2015-01-01', '%Y-%m-%d'):
			foutActive.write(location+'\t'+figureDict[location]['Long']+'\t'+figureDict[location]['Lat']+'\n')
		
	# Write maxes to an outfile
	fout.write(location+'\t'+str(maxDate)+'\t'+str(maxResult)+'\t'+maxND+'\t'+maxF+'\t'+str(len(result))+'\n')
	
	# Check if number of data is substantial
	if len(result) > subThreshold:
		# Write maxes to an outfile
		foutSubstantial.write(location+'\t'+figureDict[location]['Long']+'\t'+figureDict[location]['Lat']+'\t'+str(len(result))+'\n')
		subNum.append(len(result))

# Print summary stats
print('Ave # of samples- ', statistics.mean(subNum))
print('Ave exceedance- ', statistics.mean(exceedance))

# plt.hist(exceedance, bins=1200)
sns.distplot(exceedance, hist = False, kde = True)
# plt.show()

fout.close()
foutExceedance.close()
foutActive.close()
foutSubstantial.close()