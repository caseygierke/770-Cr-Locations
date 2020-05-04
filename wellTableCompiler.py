# wellTableCompiler.py

# This script compiles well information from the 
# Well Info- 2019-01-09- Areas & Watersheds in the IEc
# database, the Monitoring Wells dataset acquired from
# Intellus and the Chromium dataset acquired from 
# Intellus. It uses the Well Info table as a primary
# and identifies discrepencies between the three 
# datasets or within individual datasets.

# Written by Casey Gierke of Lee Wilson & Associates
# on 4/6/2020

# With Notepad++, use F5 then copy this into box
# C:\Users\Casey\Anaconda3\python.exe -i "$(FULL_CURRENT_PATH)"

# ------------------------------------------------------
# IMPORTS
# ------------------------------------------------------

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
		
# Define getLocations
def getLocations(filePath):
	# Define input file
	WI_In = open(filePath, 'r')
	# Define wellInfo dictionary
	wellInfo = {}
	# Loop through wellInfoIn
	for line in WI_In:
		# Split up input line
		cols = line.split('\t')
		if cols[0] not in wellInfo:
			wellInfo[cols[0]] = {}
	return wellInfo
	
def dictOut(dict, path):
	fout = open(path, 'w')
	# Get keys
	headers = dict['R-15'].keys()
	headers = str(headers)[12:-3].replace("', '",'\t')
	# Write header line
	fout.write(headers+'\n')
	# Loop through dictionary to write to file
	for item in dict:
		if wellInfo[item] != {}:
			# print(item)
			outString = ''
			for key in dict[item]:
				outString = outString +str(dict[item][key])+'\t'
			fout.write(outString[:-1]+'\n')
	fout.close()
	
# ------------------------------------------------------
# INPUTS
# ------------------------------------------------------

# Define path
path = os.path.abspath(os.path.dirname(__file__))
# Shorten path to one folder up
path = path[:find_last(path,os.sep)]
# # Shorten path to one folder up
# path = path[:find_last(path,os.sep)]

# # Create outfile to write to
# fout = open(path+os.sep+'Locations'+os.sep+'Well Info- Out.txt', 'w')

# # Information to populate in table
# outputHeaders = ['Location ID', 'Type', 'Latitude', 'Longitude', 'Ground Elevation', 'Geologic Unit', 'Well Installation Date', 'Total Well Depth [ft]', 'Well Diameter [in]', 'Screen Top [ft]', 'Screen Bottom [ft]', 'Geologic Unit', 'Comments', 'WELL_COMPLETION_REPORT_URL', 'Source'] 

# Which parameter are you using
parameter = 'Chromium'
# Which file type are you using
type = 'Narrowed'
# type = 'Active'

# Get spring data
springInfo = getLocations(path+os.sep+'Locations'+os.sep+'Inputs'+os.sep+'Springs.ascii')
# Get watercourse data
watercourseInfo = getLocations(path+os.sep+'Locations'+os.sep+'Inputs'+os.sep+'Watercourses.ascii')

# Get wells from Well Info- Narrowed
wellInfo = getLocations(path+os.sep+'Locations'+os.sep+'Inputs'+os.sep+type+'- Well Info.txt')

# Shorten path for getting shp files
shpPath = path[:path.find('Chromium')]
# Open Well Info source file
wellInfoIn = open(shpPath+os.sep+'GIS'+os.sep+'ascii Files'+os.sep+'Well Info- Areas & Watersheds.txt', 'r')

# Get first line
cols = wellInfoIn.readline()
cols = cols.split('\t')
headers = cols

# fout.write('Location ID	Aquifer\tLatitude\tLongitude\tGround Elevation\tGeologic Unit\tWell Installation Date\tTotal Well Depth [ft]\tWell Diameter [in]\tScreen Top [ft]\tScreen Bottom [ft]\tComments\tWELL_COMPLETION_REPORT_URL\tMonitoring Area\tWatershed\tGeologic Unit Code\tHydro Unit\tWell Info Filename\tLWA Comments\tWell Status\tCommon Name\tLocation Status\tInactive Date\tUse\tTOC Elevation\tSource\n')

# Loop through wellInfoIn
for line in wellInfoIn:

	# Split up input line
	cols = line.split('\t')
	# cols = line
	
	# # Write to outfile to check
	# fout.write(cols[0]+'\t'+cols[65]+'\t'+cols[18]+'\t'+cols[17]+'\t'+cols[7]+'\t'+cols[68]+'\t'+cols[82]+'\t'+cols[83]+'\t'+cols[101]+'\t'+cols[62]+'\t'+cols[63]+'\t'+cols[43]+', '+cols[95]+'\t'+cols[112]+'\t'+cols[114]+'\t'+cols[115][:-1]+'\t'+cols[75]+'\t'+cols[69]+'\t'+cols[112]+'\t'+cols[113]+'\t'+cols[90]+'\t'+cols[55]+'\t'+cols[35]+'\t'+cols[40]+'\t'+cols[81]+'\t'+'Well Info\n')
	
	# Define location
	location = cols[0]
	
	# Check that location is not in springs or watercourse
	# if location in springInfo or location in watercourseInfo:
	if location in watercourseInfo:
		continue
	
	# Define excluded types
	# excludedTypes = ['SS(0-1ft)', 'BH(1-10ft)', 'BH', 'WCS', 'CH', 'BHover10ft', 'AMS', 'FS', 'SPR', 'NB', 'OUT', 'WIP', 'GENERIC', 'MET_Tower', 'DWF', 'MOI', 'TEST', 'SO']
	excludedTypes = ['WCS']

	# Check that location is not excluded location type
	if cols[2] in excludedTypes:
		# print(location+' excluded because type is '+cols[2])
		continue
	
	# # Check that number of columns is correct to be sure that it read in correctly
	# if len(cols) != 116:
		# print(location)
	
	# Check if location in wellInfo dictionary
	if location in wellInfo:
		
		# Add info
		wellInfo[location] = {
			# 'Location ID', 'Type', 'Latitude', 'Longitude', 'Ground Elevation', 'Geologic Unit', 'Well Installation Date', 'Total Well Depth [ft]', 'Well Diameter [in]', 'Screen Top [ft]', 'Screen Bottom [ft]', 'Geologic Unit', 'Comments', 'WELL_COMPLETION_REPORT_URL', 'Source'
			
			'Location ID': cols[0], 
			'Aquifer': cols[65], 
			'Latitude': cols[18], 
			'Longitude': cols[17], 
			'Ground Elevation': cols[7], 
			# 'Geologic Unit': cols[68], 
			'Geologic Unit Code': cols[75], 
			'Well Installation Date': cols[82], 
			'Total Well Depth [ft]': cols[83], 
			'Well Diameter [in]': cols[101], 
			'Screen Top [ft]': cols[62], 
			'Screen Bottom [ft]': cols[63], 
			'Comments': cols[43]+', '+cols[95], 
			'WELL_COMPLETION_REPORT_URL': 'NULL', 
			'Location Type': cols[2], 
			'Monitoring Area': cols[114], 
			'Watershed': cols[115][:-1], 
			# 'Hydro Unit': cols[69], 
			# 'Well Info Filename': cols[112],
			# 'LWA Comments': cols[113], 
			'Well Status': cols[90],
			# 'Common Name': cols[55], 
			# 'Location Status': cols[35],
			'Inactive Date': cols[40], 
			# 'Use': cols[81], 
			'TOC Elevation': [84],
			'LWA Notes': '',
			'Source': 'Well Info'
			}

# fout.close()

before = len(wellInfo)
# dictOut(wellInfo, path+os.sep+'Locations'+os.sep+'Well Info- '+type+'- WI.txt')

# ------------------------------------------------------
# Add info from monitoring wells
# ------------------------------------------------------

# Get wells from Intellus Monitoring Wells- Narrowed
monitoringWells = getLocations(path+os.sep+'Locations'+os.sep+'Inputs'+os.sep+os.sep+type+'- Intellus Monitoring Wells.txt')

# Open Monitoring Wells source file
MWin = open(path+os.sep+'Locations'+os.sep+'Intellus Monitoring Wells.ascii', 'r')

# Get first line
headers = MWin.readline()
headers = headers.split('\t')

# Start discrepancy dictionary
discrepancy = {}
	
# Loop through wellInfoIn
for line in MWin:

	# Split up input line
	cols = line.split('\t')
	# cols = line
		
	# Define location
	location = cols[0]
	
	# Check that location is not in springs or watercourse
	if location in springInfo or location in watercourseInfo:
		continue
	
	# Check that it is part of the Narrowed dataset
	if location in monitoringWells:
	
		# Check if location in wellInfo dictionary
		if location not in wellInfo:
			
			# print(location)
			
			# Add info
			wellInfo[location] = {
				'Location ID': cols[0], 
				'Aquifer': cols[13], 
				'Latitude': cols[2], 
				'Longitude': cols[1], 
				'Ground Elevation': cols[3], 
				'Geologic Unit Code': cols[15], 
				'Well Installation Date': '', 
				'Total Well Depth [ft]': cols[7], 
				'Well Diameter [in]': cols[10], 
				'Screen Top [ft]': cols[11], 
				'Screen Bottom [ft]': cols[12], 
				'Comments': cols[6], 
				'WELL_COMPLETION_REPORT_URL': cols[16][:-1], 
				'Location Type': '', 
				'Monitoring Area': '', 
				'Watershed': '', 
				'Well Status': '',
				'Inactive Date': '', 
				'TOC Elevation': cols[9],
				'LWA Notes': '',
				'Source': 'Monitoring Wells'
				}
			
		else:
			
			# Create temp dictionary to compare to 
			tempDict = {
				'Location ID': cols[0], 
				'Aquifer': cols[13], 
				'Latitude': cols[2], 
				'Longitude': cols[1], 
				'Ground Elevation': cols[3], 
				'Geologic Unit Code': cols[15], 
				'Well Installation Date': '', 
				'Total Well Depth [ft]': cols[7], 
				'Well Diameter [in]': cols[10], 
				'Screen Top [ft]': cols[11], 
				'Screen Bottom [ft]': cols[12], 
				'Comments': cols[6], 
				'WELL_COMPLETION_REPORT_URL': cols[16][:-1], 
				'Location Type': '', 
				'Monitoring Area': '', 
				'Watershed': '', 
				'Well Status': '',
				'Inactive Date': '', 
				'TOC Elevation': cols[9],
				'LWA Notes': '',
				'Source': 'Monitoring Wells'
				}
			
			# Update Comments field
			if tempDict['Comments'] != 'None':
				wellInfo[location]['Comments'] = wellInfo[location]['Comments']+', '+tempDict['Comments']
	
			# Loop through keys in wellInfo
			for key in wellInfo[location]:
				# Check that key is in tempDict
				if key in tempDict:
					# Check that it is not a column we expect to be different
					if key not in ['Source', 'Comments', 'WELL_COMPLETION_REPORT_URL']:
						# Check for discrepencies
						if wellInfo[location][key] != tempDict[key]:
							discrep = True
							# Check that temp is not None
							if tempDict[key] == 'None':
								discrep = False
							# Check that temp is not blank
							if tempDict[key] == '':
								discrep = False
							# Eliminate placeholder screen depth values
							if tempDict[key] == '-9999':
								discrep = False
							# Check for slight lat long differences
							if key == 'Latitude' or key == 'Longitude':
								if round(float(wellInfo[location][key]),4) == round(float(tempDict[key]), 4):
									discrep = False
							if key == 'Ground Elevation':
								if wellInfo[location][key] != 'NULL' and tempDict[key] != 'None':
									if round(float(wellInfo[location][key]),0) == round(float(tempDict[key]), 0):
										discrep = False
								
							if discrep == True:
								# Check that wellInfo value is not NULL 
								if wellInfo[location][key] == 'NULL':
										
									# print('Updating '+location+'- '+key+' to '+tempDict[key])
									
									# Update the wellInfo info
									wellInfo[location][key] = tempDict[key]
									
									# Update notes
									if wellInfo[location]['LWA Notes'] == '':
										wellInfo[location]['LWA Notes'] = str(key)+' updated from MW'
									else:
										wellInfo[location]['LWA Notes'] = wellInfo[location]['LWA Notes'] +', '+ str(key)+' updated from MW'
									
								# Check if location is in discrepancy dictionay
								if location not in discrepancy:
									# Create a dictionary for this item
									discrepancy[location] = {'Location ID': location, 'Aquifer': '', 'Latitude': '', 'Longitude': '', 'Ground Elevation': '', 'Well Installation Date': '', 'Total Well Depth [ft]': '', 'Well Diameter [in]': '', 'Screen Top [ft]': '', 'Screen Bottom [ft]': '', 'Comments': '', 'Monitoring Area': '', 'Watershed': '', 'Geologic Unit Code': '', 'Well Status': '', 'Inactive Date': '', 'TOC Elevation': ''}
									discrepancy[location][key] = [tempDict[key]]
									discrepancy[location]['LWA Notes'] = str(key)+'- MW'
								else:
									# Check if location has that key
									if discrepancy[location][key] == '':
										discrepancy[location][key] = [tempDict[key]]
										discrepancy[location]['LWA Notes'] = discrepancy[location]['LWA Notes'] +', '+ str(key)+'- MW'
									else:
										# Check that it is new and unique
										if tempDict[key] not in discrepancy[location][key]:
											discrepancy[location][key].append(tempDict[key])
											discrepancy[location]['LWA Notes'] = discrepancy[location]['LWA Notes'] +', '+ str(key)+'- MW'
								
MWin.close()
								
after = len(wellInfo)
# dictOut(wellInfo, path+os.sep+'Locations'+os.sep+'Well Info- '+type+'- MW.txt')
# dictOut(discrepancy, path+os.sep+'Locations'+os.sep+'discrepancy- '+type+'- MW.txt')

# ------------------------------------------------------
# Add info from chromium data
# ------------------------------------------------------

# Get wells from Chromium Data- Narrowed
chromiumData = getLocations(path+os.sep+'Locations'+os.sep+'Inputs'+os.sep+os.sep+type+'- Intellus Chromium Data.txt')

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

# Open Monitoring Wells source file
# CDin = open(path+os.sep+'Locations'+os.sep+'Intellus Monitoring Wells.ascii', 'r')
CDin = open(path+os.sep+'Intellus Data'+os.sep+'EIM_EXPORT_'+downDate+'.txt','r')

# Get first line
headers = CDin.readline()
headers = headers.split('\t')

# # Start discrepancy dictionary
# discrepancy = {}
	
# Loop through wellInfoIn
for line in CDin:

	# Split up input line
	cols = line.split('\t')
	# cols = line
		
	# Define location
	location = cols[2]
	
	# Check that location is not in springs or watercourse
	if location in springInfo or location in watercourseInfo:
		# print(location)
		continue
	
	# Check that it is part of the Narrowed dataset
	if location in chromiumData:
	
		# Check if location in wellInfo dictionary
		if location not in wellInfo:
			
			# print(location)
			
			# Add info
			wellInfo[location] = {
				'Location ID': cols[2], 
				'Aquifer': '', 
				'Latitude': cols[13], 
				'Longitude': cols[14], 
				'Ground Elevation': '', 
				'Geologic Unit Code': '', 
				'Well Installation Date': '', 
				'Total Well Depth [ft]': '', 
				'Well Diameter [in]': '', 
				'Screen Top [ft]': '', 
				'Screen Bottom [ft]': '', 
				'Comments': '', 
				'WELL_COMPLETION_REPORT_URL': '', 
				'Location Type': '', 
				'Monitoring Area': '', 
				'Watershed': '', 
				'Well Status': '',
				'Inactive Date': '', 
				'TOC Elevation': '', 
				'LWA Notes': '',
				'Source': 'Chromium Data'
				}
			
		else:
			
			# Create temp dictionary to compare to 
			tempDict = {
				'Location ID': cols[2], 
				'Aquifer': '', 
				'Latitude': cols[13], 
				'Longitude': cols[14], 
				'Ground Elevation': '', 
				'Geologic Unit Code': '', 
				'Well Installation Date': '', 
				'Total Well Depth [ft]': '', 
				'Well Diameter [in]': '', 
				'Screen Top [ft]': '', 
				'Screen Bottom [ft]': '', 
				'Comments': '', 
				'WELL_COMPLETION_REPORT_URL': '', 
				'Location Type': '', 
				'Monitoring Area': '', 
				'Watershed': '', 
				'Well Status': '',
				'Inactive Date': '', 
				'TOC Elevation': '', 
				'LWA Notes': '',
				'Source': 'Chromium Data'
				}
			
			# # Update Comments field
			# tempDict['Comments'] = tempDict['Comments'].replace('NULL', '')
			# if tempDict['Comments'] != '':
				# print(tempDict['Comments'])
				
				# wellInfo[location]['Comments'] = wellInfo[location]['Comments']+', '+tempDict['Comments']
	
			# Loop through keys in wellInfo
			for key in wellInfo[location]:
				# Check that key is in tempDict
				if key in tempDict:
					# Check that it is not a column we expect to be different
					if key not in ['Source', 'Comments', 'WELL_COMPLETION_REPORT_URL']:
						# Check for discrepencies
						if wellInfo[location][key] != tempDict[key]:
							discrep = True
							# Check that temp is not None
							if tempDict[key] == 'None':
								discrep = False
							# Check that temp is not blank
							if tempDict[key] == '':
								discrep = False
							# Eliminate placeholder screen depth values
							if tempDict[key] == '-9999':
								discrep = False
							# Check for slight lat long differences
							if key == 'Latitude' or key == 'Longitude':
								if round(float(wellInfo[location][key]),4) == round(float(tempDict[key]), 4):
									discrep = False
							# if key == 'Ground Elevation':
								# if wellInfo[location][key] != 'NULL' and tempDict[key] != 'None':
									# if round(float(wellInfo[location][key]),0) == round(float(tempDict[key]), 0):
										# discrep = False
								
							if discrep == True:
								# Check that wellInfo value is not NULL 
								if wellInfo[location][key] == 'NULL':
										
									# print('Updating '+location+'- '+key+' to '+tempDict[key])
									
									# Update the wellInfo info
									wellInfo[location][key] = tempDict[key]
									
									# Update notes
									if wellInfo[location]['LWA Notes'] == '':
										wellInfo[location]['LWA Notes'] = str(key)+' updated from CD'
									else:
										wellInfo[location]['LWA Notes'] = wellInfo[location]['LWA Notes'] +', '+ str(key)+' updated from CD'
									
								# Check if location is in discrepancy dictionay
								if location not in discrepancy:
									# Create a dictionary for this item
									discrepancy[location] = {'Location ID': location, 'Aquifer': '', 'Latitude': '', 'Longitude': '', 'Ground Elevation': '', 'Well Installation Date': '', 'Total Well Depth [ft]': '', 'Well Diameter [in]': '', 'Screen Top [ft]': '', 'Screen Bottom [ft]': '', 'Comments': '', 'Monitoring Area': '', 'Watershed': '', 'Geologic Unit Code': '', 'Well Status': '', 'Inactive Date': '', 'TOC Elevation': ''}
									discrepancy[location][key] = [tempDict[key]]
									discrepancy[location]['LWA Notes'] = str(key)+'- CD'
								else:
									# Check if location has that key
									if discrepancy[location][key] == '':
										discrepancy[location][key] = [tempDict[key]]
										discrepancy[location]['LWA Notes'] = discrepancy[location]['LWA Notes'] +', '+ str(key)+'- CD'
									else:
										# Check that it is new and unique
										if tempDict[key] not in discrepancy[location][key]:
											discrepancy[location][key].append(tempDict[key])
											discrepancy[location]['LWA Notes'] = discrepancy[location]['LWA Notes'] +', '+ str(key)+'- CD'
								
CDin.close()
final = len(wellInfo)

# Write to outfile
dictOut(wellInfo, path+os.sep+'Python'+os.sep+'Locations'+os.sep+'Compiled- '+type+'.txt')
dictOut(discrepancy, path+os.sep+'Python'+os.sep+'Locations'+os.sep+'discrepancy- '+type+'- Compiled.txt')
								
# ------------------------------------------------------
# Add info from exceedances
# ------------------------------------------------------

# For active tables, loop back to include exceedance locations
if type == 'Active':
	# Check that exceedance info exists
	if os.path.exists(path+os.sep+'Python'+os.sep+'Plotting'+os.sep+'Outputs'+os.sep+'Exceedance- Compiled- '+type+'.txt'):
		
		# Get wells from Chromium Data- Narrowed
		exceedanceData = getLocations(path+os.sep+'Python'+os.sep+'Plotting'+os.sep+'Outputs'+os.sep+'Exceedance- Compiled- '+type+'.txt')

		# Loop through wellInfoIn
		for location in exceedanceData:
			
			if location not in wellInfo:
				
				print('Must add '+location)
				
				# Add info
				# * get Location Type
				wellInfo[location] = {
					# 'Location ID', 'Type', 'Latitude', 'Longitude', 'Ground Elevation', 'Geologic Unit', 'Well Installation Date', 'Total Well Depth [ft]', 'Well Diameter [in]', 'Screen Top [ft]', 'Screen Bottom [ft]', 'Geologic Unit', 'Comments', 'WELL_COMPLETION_REPORT_URL', 'Source'
					
					'Location ID': cols[0], 
					'Aquifer': cols[65], 
					'Latitude': cols[18], 
					'Longitude': cols[17], 
					'Ground Elevation': cols[7], 
					# 'Geologic Unit': cols[68], 
					'Geologic Unit Code': cols[75], 
					'Well Installation Date': cols[82], 
					'Total Well Depth [ft]': cols[83], 
					'Well Diameter [in]': cols[101], 
					'Screen Top [ft]': cols[62], 
					'Screen Bottom [ft]': cols[63], 
					'Comments': cols[43]+', '+cols[95], 
					'WELL_COMPLETION_REPORT_URL': 'NULL', 
					'Location Type': cols[2], 
					'Monitoring Area': cols[114], 
					'Watershed': cols[115][:-1], 
					# 'Hydro Unit': cols[69], 
					# 'Well Info Filename': cols[112],
					# 'LWA Comments': cols[113], 
					'Well Status': cols[90],
					# 'Common Name': cols[55], 
					# 'Location Status': cols[35],
					'Inactive Date': cols[40], 
					# 'Use': cols[81], 
					'TOC Elevation': [84],
					'LWA Notes': '',
					'Source': 'Exceedances'
					}

		
	else:
		print('Exceedance file does not exist. \n\tRun plotter to create exceedance file.')
	
# ------------------------------------------------------
# Write to outfiles
# ------------------------------------------------------

final = len(wellInfo)

# Write to outfile
dictOut(wellInfo, path+os.sep+'Python'+os.sep+'Locations'+os.sep+'Outputs'+os.sep+'Compiled- '+type+'.txt')
dictOut(discrepancy, path+os.sep+'Python'+os.sep+'Locations'+os.sep+'Outputs'+os.sep+'Discrepancy- Compiled- '+type+'.txt')
