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

# Define infile
infile = 'Compiled- Narrowed'
# input = 'Plume- Compiled- Regional'
inputPath = path+os.sep+'Python'+os.sep+'Locations'+os.sep+'Outputs'+os.sep

# Define subThreshold value (number of data points to be substantial)
subThreshold = 3

# Make dictionary for appendix figures
figureDict = {}
Dictin = open(inputPath+infile+'.txt','r')

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
fout = open(path+os.sep+'Python'+os.sep+'Locations'+os.sep+'Outputs'+os.sep+'Maxes- '+infile+'.txt','w')

# Create an outfile for storing exceedances
foutExceedance = open(path+os.sep+'Python'+os.sep+'Locations'+os.sep+'Outputs'+os.sep+'Exceedance- '+infile+'.txt','w')

# Create arrays for tracking exceedances and the results
exceedance = []
Results = []


# Create an outfile for defining active locations
foutActive = open(path+os.sep+'Python'+os.sep+'Locations'+os.sep+'Outputs'+os.sep+'Active- '+infile+'.txt','w')

# Create an outfile for defining active locations
foutSubstantial = open(path+os.sep+'Python'+os.sep+'Locations'+os.sep+'Outputs'+os.sep+'Substantial Data- '+infile+'.txt','w')
subNum = []

# ------------------------------------------------------
# COMPUTATIONS
# ------------------------------------------------------

# Define SLV value
SLV = 7.48

# Loop over inputs
for location in figureDict:

	print('Working on '+location)

	# ------------------------------------------------------
	# Query out Cr(VI) data
	sql = "SELECT SAMPLE_DATE, REPORT_RESULT AS Data, DETECTED, FILTERED FROM Chromium_Flagged WHERE LOCATION_ID = '"+location+"' AND PARAMETER_CODE = 'Cr(VI)' ORDER BY SAMPLE_DATE"
	dataVI = DB_get(sql)
		
	# Initialize arrays
	dateVI = []
	resultVI = []
	NDVI = []
	FVI = []
	daysNDVI = []
	dataNDVI = []
	daysFVI = []
	dataFVI = []

	# Loop through data
	for row in dataVI:
		
		# Check for ND = 10 condition
		if row[2] == 'N' and float(row[1]) == 10.0:
			continue
			
		# Append values
		dateVI.append(row[0])
		resultVI.append(float(row[1]))
		NDVI.append(row[2])
		FVI.append(row[3])
		
		# Check for non-detects
		if row[2] == 'N':
			daysNDVI.append(row[0])
			dataNDVI.append(float(row[1]))
		# Check for filtering
		if row[3] == 'Y':
			daysFVI.append(row[0])
			dataFVI.append(float(row[1]))
			
	# Check if result has values
	if resultVI == []:
		maxResultVI = 'No Data'
		maxDateVI = 'No Data'
		maxNDVI = 'No Data'
		maxFVI = 'No Data'
		lastVI = 'No Data'
		lastDateVI = 'No Data'
	else:
		# Append to total results
		for item in resultVI:
			Results.append(item)
		
		# Get max
		maxResultVI = max(resultVI)
		maxIndexVI = resultVI.index(maxResultVI)
		maxDateVI = dateVI[maxIndexVI]
		maxNDVI = NDVI[maxIndexVI]
		maxFVI = FVI[maxIndexVI]
		lastVI = resultVI[-1]
		lastDateVI = dateVI[-1]
		
	# ------------------------------------------------------
	# Query out Cr data
	sql = "SELECT SAMPLE_DATE, REPORT_RESULT AS Data, DETECTED, FILTERED FROM Chromium_Flagged WHERE LOCATION_ID = '"+location+"' AND PARAMETER_CODE = 'Cr' ORDER BY SAMPLE_DATE"
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
		
		# # Check for ND = 10 condition
		# if row[2] == 'N' and float(row[1]) == 10.0:
			# continue
			
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
		last = 'No Data'
		lastND = 'No Data'
		lastDate = 'No Data'
	else:
		# Append to total results
		for item in result:
			Results.append(item)
		
		# Get max
		maxResult = max(result)
		maxIndex = result.index(maxResult)
		maxDate = date[maxIndex]
		maxND = ND[maxIndex]
		maxF = F[maxIndex]
		last = result[-1]
		lastND = ND[-1]
		lastDate = date[-1]
		
		# Write exceedances to outfile
		if float(maxResult) > SLV:
			
			# Run another query to verify the exceedance is not a ND
			sql = "SELECT REPORT_RESULT AS Data FROM Chromium_Flagged WHERE LOCATION_ID = '"+location+"' AND REPORT_RESULT > "+str(SLV)+"AND DETECTED = 'Y'"
			exceedanceResult = DB_get(sql)
			
			# Check if it returns results
			if exceedanceResult != []:
				
				# Write to file
				foutExceedance.write(location+'\t'+figureDict[location]['Long']+'\t'+figureDict[location]['Lat']+'\t'+str(maxDate)+'\t'+str(maxResult)+'\t'+maxND+'\t'+maxF+'\t'+str(len(result))+'\n')
				
				# Append to exceedance list
				for item in exceedanceResult:
					exceedance.append(item[0])

		# Check if active
		if datetime.datetime(max(date).year, max(date).month, max(date).day) > datetime.datetime.strptime('2015-01-01', '%Y-%m-%d'):
			print(location)
			foutActive.write(location+'\t'+figureDict[location]['Long']+'\t'+figureDict[location]['Lat']+'\n')
		
	# Maxes
	
	# Check if max is ND
	if maxResult == 'No Data':
		fout.write(location+'\t'+figureDict[location]['Long']+'\t'+figureDict[location]['Lat']+'\t'+str(maxResult)+'\t'+str(maxDate)+'\t'+maxND+'\t'+maxF+'\t'+str(last)+'\t'+str(lastDate)+'\t'+str(maxResultVI)+'\t'+str(maxDateVI)+'\t'+str(lastVI)+'\t'+str(lastDateVI)+'\t'+str(len(result))+'\n')
	# Deal with last data ND
	if lastND == 'N':
		print(location, 'has ND for last value, querying for data that is detected')
		
		# Run a new query for maxes
		sql = "SELECT SAMPLE_DATE, REPORT_RESULT AS Data, DETECTED, FILTERED FROM Chromium_Flagged WHERE LOCATION_ID = '"+location+"' AND DETECTED = 'Y' ORDER BY SAMPLE_DATE DESC"
		lastQueryResult = DB_get(sql)
	
		# Write maxes to an outfile
		if lastQueryResult == []:
		
			last = 'No Detect Data'
			lastDate = 'No Detect Data'
		
		else:
			last = lastQueryResult[0][1]
			lastDate = lastQueryResult[0][0]
			
			# lastQueryResult[10]
			
	if maxND == 'Y':
		fout.write(location+'\t'+figureDict[location]['Long']+'\t'+figureDict[location]['Lat']+'\t'+str(maxResult)+'\t'+str(maxDate)+'\t'+maxND+'\t'+maxF+'\t'+str(last)+'\t'+str(lastDate)+'\t'+str(maxResultVI)+'\t'+str(maxDateVI)+'\t'+str(lastVI)+'\t'+str(lastDateVI)+'\t'+str(len(result))+'\n')
	if maxResult != 'No Data' and maxND == 'N':
		print(location, 'has ND for max value, querying for data that is detected')
		
		# Run a new query for maxes
		sql = "SELECT SAMPLE_DATE, REPORT_RESULT AS Data, DETECTED, FILTERED FROM Chromium_Flagged WHERE LOCATION_ID = '"+location+"' AND DETECTED = 'Y' ORDER BY Data DESC"
		maxQueryResult = DB_get(sql)
	
		# Write maxes to an outfile
		if maxQueryResult == []:
		
			maxResult = 'No Detect Data'
			maxDate = 'No Detect Data'
			maxND = 'No Detect Data'
			maxF = 'No Detect Data'
			fout.write(location+'\t'+figureDict[location]['Long']+'\t'+figureDict[location]['Lat']+'\t'+str(maxResult)+'\t'+str(maxDate)+'\t'+maxND+'\t'+maxF+'\t'+str(last)+'\t'+str(lastDate)+'\t'+str(maxResultVI)+'\t'+str(maxDateVI)+'\t'+str(lastVI)+'\t'+str(lastDateVI)+'\t'+str(len(result))+'\n')
			# fout.write(location+'\t'+figureDict[location]['Long']+'\t'+figureDict[location]['Lat']+'\tNA\tNA\tNA\tNA\t'+str(last)+'\t'+str(lastDate)+'\t'+str(maxResultVI)+'\t'+str(maxDateVI)+'\t'+str(lastVI)+'\t'+str(lastDateVI)+'\t'+str(len(result))+'\n')
		else:
			# maxQueryResult[0][0]
			maxResult = maxQueryResult[0][1]
			maxDate = maxQueryResult[0][0]
			maxND = maxQueryResult[0][2]
			maxF = maxQueryResult[0][3]
			
			# maxF[10]
			
			fout.write(location+'\t'+figureDict[location]['Long']+'\t'+figureDict[location]['Lat']+'\t'+str(maxResult)+'\t'+str(maxDate)+'\t'+maxND+'\t'+maxF+'\t'+str(last)+'\t'+str(lastDate)+'\t'+str(maxResultVI)+'\t'+str(maxDateVI)+'\t'+str(lastVI)+'\t'+str(lastDateVI)+'\t'+str(len(result))+'\n')
			# fout.write(location+'\t'+figureDict[location]['Long']+'\t'+figureDict[location]['Lat']+'\t'+str(maxResult)+'\t'+str(maxDate)+'\t'+maxND+'\t'+maxF+'\t'+str(last)+'\t'+str(lastDate)+'\t'+str(maxResultVI)+'\t'+str(maxDateVI)+'\t'+str(lastVI)+'\t'+str(lastDateVI)+'\t'+str(len(result))+'\n')
	
	# fout.write(location+'\t'+figureDict[location]['Long']+'\t'+figureDict[location]['Lat']+'\t'+str(maxResult)+'\t'+str(maxDate)+'\t'+maxND+'\t'+maxF+'\t'+str(last)+'\t'+str(lastDate)+'\t'+str(maxResultVI)+'\t'+str(maxDateVI)+'\t'+str(lastVI)+'\t'+str(lastDateVI)+'\t'+str(len(result))+'\n')
	
	# Check if number of data is substantial
	if len(result) > subThreshold:
		# Write maxes to an outfile
		foutSubstantial.write(location+'\t'+figureDict[location]['Long']+'\t'+figureDict[location]['Lat']+'\t'+str(len(result))+'\n')
		subNum.append(len(result))

# Print summary stats
print('Ave # of samples- ', statistics.mean(subNum))
print('Ave exceedance- ', statistics.mean(exceedance))

fout.close()
foutExceedance.close()
foutActive.close()
foutSubstantial.close()

# plt.hist(exceedance, bins=1200)
sns.distplot(exceedance, hist = False, kde = True, label='Exceedances')
sns.distplot(Results, hist = False, kde = True, label='All results')
plt.legend()
plt.show()