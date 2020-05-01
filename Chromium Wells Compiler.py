# Chromium Wells Compiler.py

# This script takes the .csv output from Intellus of all the 
# chromium data from LANL and compiles it into an ascii file well locations 
# ideal for generating tables and .shp files

# Scripted by Casey Gierke of Lee Wilson & Associates on 2017-06-02
# Updated 3/23/2020
# Updated 4/3/2020

# With Notepad++, use F5 then copy this into box
# C:\ProgramData\Anaconda3\python.exe -i "$(FULL_CURRENT_PATH)"

# ------------------------------------------------------
# IMPORTS
# ------------------------------------------------------

import os
import re
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

# Create finder function
def find_nth(haystack, needle, n):
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start+len(needle))
        n -= 1
    return start

# ------------------------------------------------------
# INPUTS
# ------------------------------------------------------

# Define path
path = os.path.abspath(os.path.dirname(__file__))
# Shorten path to one folder up
path = path[:find_last(path,os.sep)]
# Shorten path to one folder up
path = path[:find_last(path,os.sep)]

# Get most recent download
dates = []
for date in glob.glob(path+os.sep+'Intellus Data'+os.sep+'EIM_EXPORT_*.csv'):
    # dates.append(date[-8:-4]+date[-14:-12]+date[-11:-9])
	date = date[-14:-4]
	dates.append(date[-4:]+date[:2]+date[3:5])

# Select most recent folder
downDate = max(dates)

# Convert back to file format
downDate = downDate[-4:-2]+'_'+downDate[-2:]+'_'+downDate[:4]

print('Using input file EIM_EXPORT_'+downDate+'.csv')

# Open in file
fin = open(path+os.sep+'Intellus Data'+os.sep+'EIM_EXPORT_'+downDate+'.txt','r')

# Get first line
cols = fin.readline()
cols = cols.replace(' ','_')
cols = cols.upper()
cols = cols.split('\t')
headers = cols
	
# headers = line.split(',')

# # Adjust header row
locID_index = headers.index('LOCATION_ID')
lat_index = headers.index('LATITUDE_(DECIMAL)')
long_index = headers.index('LONGITUDE_(DECIMAL)')
type_index = headers.index('SAMPLE_TYPE')

# sampleDate_index = headers.index('Sample Date')
# result_index = headers.index('Report Result')
# units_index = headers.index('Report Units')
# labQual_index = headers.index('Lab Qualifier')
# valQual_index = headers.index('Validation Qualifier\n')
# detected_index = headers.index('Detected')
# filtered_index = headers.index('Filtered')

# # Set up a dummy initial lastLocID
# lastLocID = headers[locID_index]

# Create outfiles
fout = open(path+os.sep+'Python'+os.sep+'Locations'+os.sep+'Intellus Chromium Data Locations- All.ascii','w')
foutReport = open(path+os.sep+'Python'+os.sep+'Locations'+os.sep+'Intellus Chromium Data Locations- Report.ascii','w')
foutDiscrepency = open(path+os.sep+'Python'+os.sep+'Locations'+os.sep+'Intellus Chromium Data Locations- Discrepencies.ascii','w')

# # Write header line
# foutReport.write(headers[0]+'\t'+headers[lat_index]+'\t'+headers[long_index]+'\t'+'Type\tTop Screen\tBottom Screen\tGeologic Unit'+'\n')

# Initiate empty locations list
locations = []

# Initiate empty locations list
locationDict = {}

# Loop through to populate dictionary
for line in fin:
	
	# Split up line
	# line = line.replace('"','')
	columns = line.split('\t')
	
	# Remove quotation marks
	for item in columns:
		# Get index
		index = columns.index(item)
		columns[index] = item.replace('"','')
		
	# Assign values
	locID = columns[locID_index]
	# Check that it is not blank
	if locID == 'Blank':
		continue
		
	# lat = columns[lat_index]
	# long = columns[long_index]
	lat = str(round(float(columns[lat_index]),4))
	long = str(round(float(columns[long_index]),4))
	sampleType = columns[type_index]
	
	# Update dictionary
	if locID not in locationDict:
		locationDict[locID] = [lat, long, sampleType]
	else:
		if locationDict[locID][0] != lat:
			# print(locID+' lat info inconsistent.')
			print(locID+'- Lat\t'+locationDict[locID][0]+'\t'+lat)
			foutDiscrepency.write(locID+'- Lat\t'+locationDict[locID][0]+'\t'+lat+'\n')
		if locationDict[locID][1] != long:
			# print(locID+' long info inconsistent.')
			print(locID+'- Long\t'+locationDict[locID][1]+'\t'+long)
			foutDiscrepency.write(locID+'- Long\t'+locationDict[locID][1]+'\t'+long+'\n') 
	
for loc in locationDict:
	if locationDict[loc][2] == 'WG':
		fout.write(loc+'\t'+locationDict[loc][0]+'\t'+locationDict[loc][1]+'\n')

foutDiscrepency.close()
fout.close()

# # Open a loop to go through the file
# for line in fin:
	
	# # Split up line
	# line = line.replace('"','')
	# columns = line.split(',')
	
	# # Assign values
	# locID = columns[locID_index]
	# lat = columns[lat_index]
	# long = columns[long_index]
	
	# # sampleDate = columns[sampleDate_index]
	# # result = columns[result_index]
	# # units = columns[units_index]
	# # labQual = columns[labQual_index]
	# # valQual = columns[valQual_index][:-1]
	# # detected = columns[detected_index]
	# # filtered = columns[filtered_index]

	# # # This deals with the header line
	# # if i == 0: 
		# # # Columns = line[3:].split('  +')  
		# # Columns = re.split(',',line[3:])  
		# # # I use from 3 because it has a \xef\xbb\xbf.  This is a 
		# # # Unicode "Byte Order Mark (BOM)" indicating the files is UTF-8.
		# # File.append(Columns[0])
	
	# # # This deals with the actual data
	# # if i > 0:
		# # Columns = re.split(',',line)  
		
		# # File.append(Columns[0])
		# # # Set a condition so that a new file will be opened when the data 
		# # # file enters a new well
		
	# if locID != lastLocID:
		# # # It closes the dummy file that I opened and opens it again to rewrite it
		# # fout.close()
		# # # Open a new file with the well name to write and save to
		# # fout = open(path+os.sep+'Data'+os.sep+'txt Files'+os.sep+locID+'.txt','w')
		
		# # Check if new locID in list and add if not
		# if locID not in locations:
			# locations.append(locID)
			
			# # And write to out file
			# fout.write(locID+'\t'+lat+'\t'+long+'\n')
			
			# # Check if it is in the wellDict
			# if locID in wellDict:
				# foutReport.write(locID+'\t'+lat+'\t'+long+'\t'+wellDict[locID]['info']+'\n')
			
	# # # Write the file so that the information is tab delimited
	# # if units == 'ug/L' or 'ppb':
		# # # fout.write(Columns[1][:10]+'\t'+Columns[2]+'\t'+Columns[6]+'\t'+Columns[7])
		# # fout.write(sampleDate+'\t'+ result+'\t'+ detected+'\t'+ filtered+'\n')
	# # i = i+1
	# lastLocID = locID
		
# fout.close()
# foutReport.close()
	


