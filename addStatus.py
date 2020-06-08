# addStatus.py

# This script adds Active, Exceedance and Substantial 
# Data fields from the files created by the SummaryStats.py 
# file to the Compiled- Narrowed.txt dataset

# Written by Casey Gierke of Lee Wilson & Associates
# on 5/1/2020

# With Notepad++, use F5 then copy this into box
# C:\Users\Casey\Anaconda3\python.exe -i "$(FULL_CURRENT_PATH)"

# ------------------------------------------------------
# IMPORTS
# ------------------------------------------------------

import os
import glob
import shapefile as shp
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

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
	
# Define getLocations
def getMax(filePath):
	# Define input file
	WI_In = open(filePath, 'r')
	# Define wellInfo dictionary
	wellInfo = {}
	# Loop through wellInfoIn
	for line in WI_In:
		# Split up input line
		cols = line.split('\t')
		if cols[0] not in wellInfo:
			wellInfo[cols[0]] = {'Max': cols[3], 'Date':cols[4], 'Last': cols[7], 'Last Date': cols[8], 'Max VI': cols[9], 'Date VI':cols[10], 'Last VI': cols[11], 'Last Date VI': cols[12],'Number': cols[13][:-1]}
	return wellInfo

def dictOut(dict, path):
	fout = open(path, 'w')
	# Write header line
	fout.write(headers[:-1]+'\tMax\tMax Date\tLast\tLast Date\tMax Hex\tMax Date Hex\tLast Hex\tLast Date Hex\tLength\tActive\tExceedance\tSubstantial Data\n')
	# Loop through dictionary to write to file
	for item in dict:
		fout.write(dict[item])
	fout.close()
	
def addToDict(inFile, source, reasonCode):
	for location in wellData:
		if location in inFile:
			wellData[location] = wellData[location][:-1]+'\t'+reasonCode+'\n'
		else:
			wellData[location] = wellData[location][:-1]+'\t'+'\n'
			
def addMax(inFile, source):
	for location in wellData:
		if location in inFile:
			wellData[location] = wellData[location][:-1]+'\t'+inFile[location]['Max']+'\t'+inFile[location]['Date']+'\t'+inFile[location]['Last']+'\t'+inFile[location]['Last Date']+'\t'+inFile[location]['Max VI']+'\t'+inFile[location]['Date VI']+'\t'+inFile[location]['Last VI']+'\t'+inFile[location]['Last Date VI']+'\t'+inFile[location]['Number']+'\n'
			
# ------------------------------------------------------
# INPUTS
# ------------------------------------------------------

# Define path
path = os.path.abspath(os.path.dirname(__file__))
# Shorten path to one folder up
path = path[:find_last(path,os.sep)]

# Define parameters you are using
# parameter = 'Chromium'
# Which file type are you using
type = 'Compiled- Narrowed'
# # type = 'Active'

# # Define dictionary
# wellInfo = {}

# Create wellData dictionary
wellData = getLocations(path+os.sep+'Locations'+os.sep+'Outputs'+os.sep+type+'.txt')

# Open Well Info source file
compiledIn = open(path+os.sep+'Locations'+os.sep+'Outputs'+os.sep+type+'.txt', 'r')

# Get first line
cols = compiledIn.readline()
headers = cols

# Populate wellData dictionary
for line in compiledIn:
	# print(line)
	cols = line.split('\t')
	location = cols[0]
	
	wellData[location] = line

# For some reason, Location ID gets into the wellData dictionary: remove it
if 'Location ID' in wellData:
	del wellData['Location ID']
	
# ------------------------------------------------------
# Add columns based on summary stats
# ------------------------------------------------------
# ------------------------------------------------------
# Get wells from Maxes
maxInfo = getMax(path+os.sep+'Locations'+os.sep+'Outputs'+os.sep+'Maxes- '+type+'.txt')

# Add locations from active to the wellInfo dictionary
# addMax(maxInfo, wellData, wellInfo)
addMax(maxInfo, wellData)

# ------------------------------------------------------
# Get wells from Active
activeInfo = getLocations(path+os.sep+'Locations'+os.sep+'Outputs'+os.sep+'Active- '+type+'.txt')

# Add locations from active to the wellInfo dictionary
addToDict(activeInfo, wellData, 'Active')

# ------------------------------------------------------
# Get wells from Exceedance
exceedanceInfo = getLocations(path+os.sep+'Locations'+os.sep+'Outputs'+os.sep+'Exceedance- '+type+'.txt')

# Add locations from exceedance to the wellInfo dictionary
addToDict(exceedanceInfo, wellData, 'Exceedance')

# ------------------------------------------------------
# Get wells from Substantial Data
substantialInfo = getLocations(path+os.sep+'Locations'+os.sep+'Outputs'+os.sep+'Substantial Data- '+type+'.txt')

# Add locations from substantial to the wellInfo dictionary
addToDict(substantialInfo, wellData, 'Substantial')

# # ------------------------------------------------------
# # Update watershed column
# # ------------------------------------------------------

# #Open Shapefile with shapes to check points against
# sf = shp.Reader('C:'+os.sep+'Projects'+os.sep+'770- LANL'+os.sep+'GIS'+os.sep+'Chromium'+os.sep+'Extended Chromium Examination Area'+os.sep+"Watersheds- Revised") 

# #Read records in shapefile
# sfRec = sf.records() 

# n = 0
# coorDict = {}
# matplotDict = []
# watershedFinal = {}

# #Iterate through shapes in shapefile
# for shape in sf.shapeRecords(): 
	# #Initially for use in matplotlib to check shapefile
	# x = [point[0] for point in shape.shape.points[:]] 
	# #Initially for use in matplotlib to check shapefile
	# y = [point[1] for point in shape.shape.points[:]] 

	# for point in x:
		# #Convert coordinates to be read by Shapely pkg
		# matplotDict.append((x[x.index(point)],y[x.index(point)])) 

	# #Store shape in dictionary with key of watershedcipality
	# watershedFinal[sfRec[n][1]] = Polygon(matplotDict) 

	# #refresh coordinate store for next shape   
	# matplotDict = [] 
	# n += 1 

# ------------------------------------------------------
# Write to outfiles
# ------------------------------------------------------

# Write to outfile
dictOut(wellData, path+os.sep+'Locations'+os.sep+'Outputs'+os.sep+type+'- For Watersheds.txt')
