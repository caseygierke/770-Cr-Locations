# Intellus Locations Upacker.py

# With Notepad++, use F5 then copy this into box
# C:\Users\Casey\Anaconda3\python.exe -i "$(FULL_CURRENT_PATH)"

# ------------------------------------------------------
# IMPORTS
# ------------------------------------------------------

import pandas as pd
import os

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
		
# ------------------------------------------------------
# INPUTS
# ------------------------------------------------------

# Define path
path = os.path.abspath(os.path.dirname(__file__))
# Shorten path to one folder up
path = path[:find_last(path,os.sep)]
# Shorten path to one folder up
path = path[:find_last(path,os.sep)]

# Define input
input = 'Springs'
input = 'Watercourses'

# Define input file
fin = path+os.sep+'Intellus Data'+os.sep+input+'.json'

# Read in input file
df = pd.read_json(fin)

# Create an out file to write to
fout = open(path+os.sep+'Python'+os.sep+'Locations'+os.sep+input+'.ascii', 'w')

# # Write headers to file
# fout.write('locationID	LONGITUDE	LATITUDE	GROUND_ELEVATION	LOCATION_DESC	LOCATION_COMMENTS	AQUIFER	HYDROSTRATIGRAPHIC_UNIT\n')

# -------------------------------------------------
for item in df['layers'][0]['featureSet']['features']:
	
	# print(item['attributes']['locationID'])
	
	# Check for problems in LOCATION_COMMENTS
	if item['attributes']['LOCATION_COMMENTS'] and '\n' in item['attributes']['LOCATION_COMMENTS']:
		# Replace problematic new line character
		item['attributes']['LOCATION_COMMENTS'] = item['attributes']['LOCATION_COMMENTS'].replace('\n',' ')
	if item['attributes']['LOCATION_COMMENTS'] and '\r' in item['attributes']['LOCATION_COMMENTS']:
		# Replace problematic new line character
		item['attributes']['LOCATION_COMMENTS'] = item['attributes']['LOCATION_COMMENTS'].replace('\r',' ')
		
	fout.write(
			item['attributes']['locationID']+'\t'+
			str(item['attributes']['LONGITUDE'])+'\t'+
			str(item['attributes']['LATITUDE'])+'\t'+
			str(item['attributes']['GROUND_ELEVATION'])+'\t'+
			# str(item['attributes']['ESTABLISHING_DATE'])+'\t'+
			# str(item['attributes']['SURVEY_DATE'])+'\t'+
			# str(item['attributes']['ESTABLISHING_COMPANY'])+'\t'+
			# str(item['attributes']['SURVEYING_COMPANY'])+'\t'+
			# str(item['attributes']['SURVEYED_BY'])+'\t'+
			str(item['attributes']['LOCATION_DESC'])+'\t'+
			# str(item['attributes']['RECORD_SOURCE'])+'\t'+
			str(item['attributes']['LOCATION_COMMENTS'])+'\t'+
			# str(item['attributes']['WELL_TOTAL_DEPTH'])+'\t'+
			# str(item['attributes']['DEPTH_UNITS'])+'\t'+
			# str(item['attributes']['TOP_OF_CASING_ELEVATION'])+'\t'+
			# str(item['attributes']['WELL_DIAMETER'])+'\t'+
			# str(item['attributes']['PERFORATION_ZONE_START_DEPTH'])+'\t'+
			# str(item['attributes']['PERFORATION_ZONE_END_DEPTH'])+'\t'+
			str(item['attributes']['AQUIFER'])+'\t'+
			str(item['attributes']['HYDROSTRATIGRAPHIC_UNIT'])+'\n'
			# str(item['attributes']['GEOLOGICAL_UNIT_CODE'])+'\t'+
			# str(item['attributes']['WELL_COMPLETION_REPORT_URL'])+'\n'
	)
		
fout.close()
	
	